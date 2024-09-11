# V-ZUG Home Assistant Integration

**V-ZUG Integration** for Home Assistant allows you to monitor and control V-ZUG appliances (such as dishwashers and ovens) directly from your Home Assistant instance.

## Features

- Monitor the status of your V-ZUG dishwasher and oven.
- Fetch real-time updates about the appliance's program, status, and other attributes.
- Simple configuration through Home Assistant's integrations panel.

## Installation

### HACS (Home Assistant Community Store)

1. Ensure you have [HACS](https://hacs.xyz) installed in your Home Assistant instance.
2. Go to **HACS** > **Integrations**.
3. Click on the three dots menu in the top right corner and select **Custom Repositories**.
4. Add the following repository URL: `https://github.com/jakal1989/Home_assistant` and select **Integration**.
5. Click **Add**.
6. Find "V-ZUG Integration" in the HACS integrations list and click **Install**.

### Manual Installation

1. Download the repository as a ZIP file and extract it.
2. Copy the `vzug` folder to your Home Assistant `custom_components` directory:
   ```plaintext
   <config directory>/custom_components/vzug/
where <config directory> is the directory where your configuration.yaml file is located. 3. Restart Home Assistant.

Configuration
In Home Assistant, go to Settings > Devices & Services.
Click on Add Integration and search for "V-ZUG".
Follow the instructions to configure the IP addresses of your V-ZUG devices (dishwasher and/or oven).
Configuration Options
Option	Description
Dishwasher IP Address	The IP address of your V-ZUG dishwasher.
Oven IP Address	The IP address of your V-ZUG oven.
Sensors Provided
The integration provides the following sensors for each appliance:

Device Name
Serial Number
Inactive State
Program
Status
Program End Time
End Time
End Type
Device UUID
Example Use Case
You can use these sensors in your automations or dashboards to monitor the status of your V-ZUG appliances.

Troubleshooting
Make sure that the IP addresses of your devices are correct and that they are reachable on your network.
Check the Home Assistant logs for any errors related to the V-ZUG integration.
Feedback and Contributions
If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the GitHub repository.

License
This project is licensed under the MIT License.

### Erläuterung des Inhalts:

- **Titel und Beschreibung:** Eine kurze Erklärung der Integration und ihrer Funktionalitäten.
- **Features:** Beschreibt die Hauptfunktionen der Integration.
- **Installation:** Anweisungen zur Installation der Integration über HACS und manuell.
- **Konfiguration:** Beschreibt, wie die Integration konfiguriert wird, nachdem sie installiert ist.
- **Bereitgestellte Sensoren:** Liste der Sensoren, die durch die Integration zur Verfügung gestellt werden.
- **Troubleshooting:** Tipps zur Fehlerbehebung.
- **Feedback und Contributions:** Link zum GitHub-Repository für Rückmeldungen und Beiträge.
- **Lizenz:** Informationen zur Lizenzierung des Projekts.

Kopiere einfach den obigen Text in eine Datei mit dem Namen `README.md` und füge sie deinem GitHub-Repository hinzu.
