import time
import ssl
import json
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt


aws_endpoint = "YOUR_AWS_IOT_ENDPOINT"
aws_port = 8883
cert_path = "/home/raspberry/certs/"

ca_path = cert_path + "AmazonRootCA1.pem"
cert_path_crt = cert_path + "YOUR_CERTIFICATE_FILENAME.pem.crt"
key_path = cert_path + "YOUR_PRIVATE_KEY_FILENAME.pem.key"
mqtt_topic = "rpi/sensor"



mqtt_client = mqtt.Client()
mqtt_client.tls_set(ca_certs=ca_path,
                    certfile=cert_path_crt,
                    keyfile=key_path,
                    tls_version=ssl.PROTOCOL_TLSv1_2)

mqtt_client.connect(aws_endpoint, aws_port)
mqtt_client.loop_start()


if __name__ == "__main__":
    master = None
    try:
        serial_port = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            bytesize=8,
            parity='N',
            stopbits=1,
            xonxoff=0
        )

        master = modbus_rtu.RtuMaster(serial_port)
        master.set_timeout(2.0)
        master.set_verbose(True)

        dict_payload = dict()

        influx_token = "YOUR_INFLUXDB_TOKEN"
        influx_org = "olcum"
        influx_bucket = "sensor"
        influx_url = "http://localhost:8086"

        client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        while True:
            data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

            dict_payload["voltage"] = data[0] / 10.0
            dict_payload["current_A"] = (data[1] + (data[2] << 16)) / 1000.0
            dict_payload["power_W"] = (data[3] + (data[4] << 16)) / 10.0
            dict_payload["energy_Wh"] = data[5] + (data[6] << 16)
            dict_payload["frequency_Hz"] = data[7] / 10.0
            dict_payload["power_factor"] = data[8] / 100.0
            dict_payload["alarm"] = data[9]

            str_payload = json.dumps(dict_payload, indent=2)
            print(str_payload)

            point = (
                Point("electric_measurement")
                .field("voltage", dict_payload["voltage"])
                .field("current", dict_payload["current_A"])
                .field("power", dict_payload["power_W"])
                .field("energy", dict_payload["energy_Wh"])
                .field("frequency", dict_payload["frequency_Hz"])
                .field("power_factor", dict_payload["power_factor"])
                .field("alarm", dict_payload["alarm"])
            )

            write_api.write(bucket="sensor", org="olcum", record=point)

            mqtt_client.publish(mqtt_topic, str_payload)
            print(f"Published to AWS IoT topic {mqtt_topic}")

            time.sleep(30)

    except KeyboardInterrupt:
        print("Exiting PZEM script.")
    except Exception as e:
        print("Error:", e)
    finally:
        if master:
            master.close()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
