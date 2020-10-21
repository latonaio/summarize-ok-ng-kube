DEVICE = "hades"
SERVICE_BROKER_NAME = "ServiceBroker"
SERVICE_BROKER_DATA = f"/home/toyota/{DEVICE}/Data/service-broker"
STOP_SERVICE = "WorkObjectDetection"

MICROSERVICE_NAME = 'WorkObjectDetection'
MICROSERVICE_DIRECTORY_NAME = 'work-object-detection'
NEXT_SERVICES = {
    'service_name': 'ControlYaskawaRobotW',
    'directory_name': 'control-yaskawa-robot-w',
    'device': DEVICE
}
