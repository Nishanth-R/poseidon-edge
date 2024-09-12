#include "WiFi.h"
#include "StreamIO.h"
#include "VideoStream.h"
#include "NNFaceDetection.h"
#include "VideoStreamOverlay.h"
#include <PubSubClient.h>

#define CHANNEL     0
#define CHANNELNN   3

#define NNWIDTH     576
#define NNHEIGHT    320

VideoSetting config(VIDEO_FHD, 30, VIDEO_H264, 0);
VideoSetting configNN(NNWIDTH, NNHEIGHT, 10, VIDEO_RGB, 0);
NNFaceDetection facedet;
StreamIO videoStreamer(1, 1);
StreamIO videoStreamerNN(1, 1);

const char* ssid = "YourSSID";
const char* password = "YourPassword";

const char* mqtt_server = "your_mqtt_broker_ip";
const char* mqtt_topic = "face_detection/image";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
    Serial.begin(115200);

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // Initialize camera
    Camera.configVideoChannel(CHANNEL, config);
    Camera.configVideoChannel(CHANNELNN, configNN);
    Camera.videoInit();

    // Configure face detection
    facedet.configVideo(configNN);
    facedet.setResultCallback(FDPostProcess);
    facedet.modelSelect(FACE_DETECTION, NA_MODEL, DEFAULT_SCRFD, NA_MODEL);
    facedet.begin();

    // Configure StreamIO objects
    videoStreamer.registerInput(Camera.getStream(CHANNEL));
    videoStreamerNN.registerInput(Camera.getStream(CHANNELNN));
    videoStreamerNN.registerOutput(facedet);

    // Start video channels
    Camera.channelBegin(CHANNEL);
    Camera.channelBegin(CHANNELNN);

    // Set up MQTT
    client.setServer(mqtt_server, 1883);
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
}

void FDPostProcess(std::vector<FaceDetectionResult> results) {
    uint16_t im_h = config.height();
    uint16_t im_w = config.width();

    printf("Total number of faces detected = %d\r\n", facedet.getResultCount());

    if (facedet.getResultCount() > 0) {
        // Capture current frame
        uint8_t* buffer;
        int len = Camera.captureFrame(CHANNEL, &buffer);

        if (len > 0) {
            // Convert to JPEG
            uint8_t* jpegBuffer;
            int jpegLen = Camera.encodeJpeg(buffer, len, &jpegBuffer);

            if (jpegLen > 0) {
                // Send JPEG over MQTT
                client.publish(mqtt_topic, jpegBuffer, jpegLen, true);
                Serial.println("Face detected image sent via MQTT");
            }

            free(jpegBuffer);
        }
    }
}

void reconnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        if (client.connect("ESP32CAM")) {
            Serial.println("connected");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}
