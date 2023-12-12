# FSST Projekt

## Aufgabenstellung
In Python ein Sinus Signal erzeugen dieses per MQTT genauer gesagt Mosquito an einen Client schicken. Dieser dann das ganze auf eine Art Visualisiert und an eine Datenbank wie besprochen InfluxDB sendet. Mithilfe der InfluxDB Datenbank kann das ganze mit Grafana auch nochmal Grafisch dargestellt werden. Zum Schluss soll eine Bibliothek die eine Solaranlage eines Hauses Simuliert verwendet werden, die dann dementsprechend an InfluxDB geschickt und per Grafana Visualisiert wird.

## Mosquito MQTT
#### Aufsetzen
Eclipse Mosquito kann man downloaden unter: https://mosquitto.org/download/
Nachdem man den Installer ausgeführt hat findet man unter den Mosquitto Broker: 
	**C:/Programme/mosquitto/**
In der Konsole muss man zum Ordner navigieren und mit dieser Zeile ausführen:
	
	mosquitto -v
Sobald diese Schritte erfüllt sind ist der Mosquitto Broker **fertig** aufgesetzt.
#### Sender
Mosquito MQTT ist ein Broker auf den man Topics erstellen und subscriben kann. Um das ganze in Python umzusetzen wird die **paho-mqtt** library verwendet. Bei MQTT wird meistens der Port 1883 für Datentransfer verwendet und der Broker läuft am localhost.

	client = mqtt.Client("SinusPublisher")  
	client.connect(broker, port)
Hier wird zB. ein neuer Client angelegt und zum Broker verbunden. Ab diesem Zeitpunkt kann man auf seinen Mosquito MQTT Broker **publishen**, in diesem Fall die Sinuswerte. 
	
	while True:
		sin_value = amplitude=1 * phase
		client.publish(topic, payload=sin_value)
		phase += 0.1
		time.sleep(0.5)
		
Um den Sinus zu berechnen verwende ich diese Formel, die Sinus Werte werden direkt nach berechnung auf das **Topic** veröffentlicht. Jeder andere Client der dieses Topic abboniert hat, bekommt stetig **2 mal** pro Sekunde einen Sinuswert den man verarbeiten kann.
#### Empfänger
Der Sinuswerte Empfänger muss immer, wenn ihn was geschickt wird reagieren, also ist ein **Event Handler** die beste Lösung. 
	
	client = Client("SinusSubscriber")  
	client.connect(broker, port)  
	client.subscribe(topic)  
	client.on_message = ReceiveSinus
	
Mithilfe von einem bereits in paho eingebauten Event **on_message** kann man ganz einfach einen Event Handler einbauen.

	def ReceiveSinus(client, userdata, message):  
    value = float(message.payload.decode())  
    print("Received Sinus, Value:", value)
 Receive Sinus ist eine Methode die den Sinuswert **empfängt** und **decodiert**. Somit kann der Wert ausgegeben und verarbeitet werden.
## InfluxDB
#### Aufsetzen
InfluxDB installieren: https://docs.influxdata.com/influxdb/v2/install/?t=Windows
Nachdem die Installation erfolgreich war bekommt man einen InfluxDB Ordner mit einer **influxd.exe**. Mit der Konsole wieder in den InfluxDB Ordner navigieren und dann folgendes ausführen:
	
	influxd setup
Somit wird der  lokale InfluxDB Server auf Port 8086 laufen. Auf dem Server muss man sich Anmelden/Registrieren und man muss auch einen Token implementieren der vollen Zugriff auf die InfluxDB API ermöglichen. 
	
	token = "L1XwTzFrMM-v3LiWuCMknySKtoJPH_ay_OBfQ8isTl6Q7lUDJ81SxTBh6iFQJPYuiwDqj3LNtXtYBzteSVj1qg=="  
	org = "Organisation Name"  
	url = "http://localhost:8086"
Hier werden einige Variablen definiert um die Eingabe zu erleichern.

	write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)  
	write_api = write_client.write_api(write_options=SYNCHRONOUS)  
	query_api = write_client.query_api()
Hier werden die **Write** als auch **Query** API initialisiert um Datentransfer zwischen Python und InfluxDB zu ermöglichen.
#### Senden
Auf InfluxDB kann man einen neuen Bucket erstellen wo Werte gespeichert werden. 

	def ReceiveSinus(client, userdata, message):  
	    value = float(message.payload.decode())  
	    print("Received Sinus, Value:", value)  
	    point = (  
	        Point("Received")  
	        .tag("Sin_Val", "Value")  
	        .field("MeasurementPoint", value)  
	    )  
	    write_api.write(bucket=bucket, org="Python is Trash", record=point)
In einem Point werden die Namen und Werte gespeichert von einem Empfangenen Wert. Mithilfe der **Write** API wird der kurzvorher erstellte Punkt an die InfluxDB Datenbank gesendet.


