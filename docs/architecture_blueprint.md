# Smart City Zone-Controller Deployment Blueprint

## Task 9 — Distributed Architecture and Communication Plan

### Architecture Choice: Client-Server

I would use a **Client-Server architecture** for the Smart City platform. The three zone controllers in Zone-A, Zone-B, and Zone-C act as clients, while the central Smart City Operations dashboard and its backend services act as the server. The **scheduler and Banker's-Algorithm engine from Part 1** would run on the zone-controller side as the fixed compute core for scheduling sensor-processing jobs and checking resource safety.

This architecture is suitable for the following reasons:

- **Transparency:** The central server provides a common point for collecting and presenting information from all three zones. Operators can view alerts and sensor information without directly interacting with each zone controller.
- **Fault tolerance:** A problem with one zone controller does not have to stop the other zone controllers from operating their local workloads. The **scheduler and Banker's-Algorithm engine from Part 1** can continue running locally on the affected controller while communication with the central dashboard is unavailable.
- **Scalability:** Additional zone controllers can be added as new clients without redesigning the whole architecture. The central backend can also be scaled as the number of zones and sensor messages increases.
- **Single point of failure:** The main weakness is that the central server can become a single point of failure for centralized monitoring. To reduce this risk, the server should use redundancy and failover so that a failure does not permanently stop dashboard operations.

### Communication Plan

#### (a) Real-time public-safety alert

**Communication type:** Asynchronous  
**Protocol:** MQTT

When a zone controller detects a real-time public-safety event, it should publish an alert asynchronously using MQTT. The **scheduler and Banker's-Algorithm engine from Part 1** can continue processing its local sensor-processing jobs without waiting for the Smart City Operations dashboard to respond. MQTT is suitable because it uses a lightweight publish/subscribe model and is designed for IoT devices and event-driven communication.

For example:

```text
Zone Controller
      |
      | MQTT publish
      v
MQTT Broker
      |
      v
Smart City Operations Dashboard


### Why these choices fit the marking criteria

| Requirement                | Choice                   |
|----------------------------|--------------------------|
| Architecture               | **Client-Server**        |
| Transparency               |        ✅               |
| Fault tolerance            |        ✅               |
| Scalability                |        ✅               |
| Single point of failure    |        ✅               |
| Public-safety alert        | **Asynchronous + MQTT**  |
| Daily sensor log           | **Asynchronous + HTTPS** |
| Part 1 engine explicitly referenced |  ✅             |

**Important:** Keep **Client-Server** as the only architecture choice.
Don't mention Hybrid or Peer-to-Peer as alternative architecture choices in the document,
because the task says to pick **exactly one**.
```

## Task 10 — VPC-Based Network Boundary

### VPC and Subnet Design

I would use **one VPC containing three separate subnets**, with one subnet dedicated to each zone:

- Zone-A → Zone-A subnet
- Zone-B → Zone-B subnet
- Zone-C → Zone-C subnet

Using one VPC provides a common private network boundary for the Smart City platform, while the three subnets provide logical isolation between the individual zones. A VPC is customizable because its IP address ranges, subnets, routing rules, and security controls can be designed according to the platform's requirements. This design also makes it easier to manage the three zones centrally without creating and maintaining three completely separate VPCs.

The **scheduler and Banker's-Algorithm engine from Part 1** would run on the zone-controller resources inside their respective isolated subnets.

### Network-Level Control Enforcing the Boundary

The specific control that prevents Zone-A resources from being reached directly by Zone-B is a **firewall/security-group rule that denies inbound traffic from the Zone-B subnet's CIDR range to the Zone-A subnet's resources**.

For example, if Zone-B uses the CIDR range `10.0.2.0/24`, the security group protecting Zone-A resources would contain a rule that denies traffic originating from `10.0.2.0/24`.

Therefore:

```text
Zone-A Subnet
10.0.1.0/24
       |
       |  DENY inbound traffic
       |  from 10.0.2.0/24
       X
       |
Zone-B Subnet
10.0.2.0/24
```
## Task 11 — Network Security Objectives and Controls

The following controls protect the Smart City platform and the **scheduler and Banker's-Algorithm engine from Part 1** at different points of the network and system architecture.

| Network-Security Objective | Specific Control / Technology | How It Protects the Platform |
|---|---|---|
| **Protect sensitive data** | **AES-256 encryption at rest** | Sensor logs, configuration data, and the **scheduler and Banker's-Algorithm engine from Part 1** data stored on zone-controller systems are encrypted using AES-256. This prevents unauthorized users from reading the stored data if a device or storage system is compromised. |
| **Authentication** | **Multi-Factor Authentication (MFA)** | MFA requires operators to provide more than one authentication factor before accessing the Smart City platform. This reduces the risk of an attacker gaining access using only a stolen username and password. |
| **Authorization** | **Role-Based Access Control (RBAC)** | RBAC restricts users according to their assigned roles and permissions. For example, a zone operator can manage their zone's resources without being given permission to modify the **scheduler and Banker's-Algorithm engine from Part 1** in another zone. |
| **Prevent cyber attacks** | **Web Application Firewall (WAF)** | A WAF filters and blocks malicious HTTP/HTTPS requests before they reach the Smart City application services. It can help protect the platform from attacks such as SQL injection and cross-site scripting. |
| **Secure communication** | **TLS 1.3** | TLS 1.3 encrypts data exchanged between zone controllers and central services. This protects sensor information and public-safety alerts from being intercepted or modified while in transit. |
| **Ensure availability** | **Load balancer with redundant servers** | A load balancer distributes requests across multiple backend servers so that one server failure does not make the Smart City dashboard unavailable. This also allows the platform to handle increased traffic without overloading a single server. |

These controls work together to protect the three zone controllers, their sensor data, and the **scheduler and Banker's-Algorithm engine from Part 1** while maintaining secure and reliable communication with the central Smart City platform.

## Task 12 — IAM Roles and Data Protection

### IAM Role Table

The IAM design follows the principle of least privilege so that each user receives only the permissions required for their responsibilities. The **scheduler and Banker's-Algorithm engine from Part 1** remains protected from unauthorized modification.

| IAM Role | Specific Permission Set |
|---|---|
| **Zone Operator** | Can view sensor data, view job status, submit or monitor jobs for their assigned zone, and view alerts. Cannot modify IAM roles or access resources belonging to other zones. |
| **City Dashboard Admin** | Can view data from all three zones, manage dashboard configuration, acknowledge public-safety alerts, and manage platform-level operational settings. Cannot directly modify the source code of the **scheduler and Banker's-Algorithm engine from Part 1**. |
| **Auditor** | Has read-only access to sensor logs, job execution records, security logs, and resource-allocation records. Cannot create, modify, delete, or execute jobs. |

This role-based permission model limits the impact of a compromised account because users cannot access resources outside their assigned responsibilities.

### Data-Protection Map

| Data State | Protection Technique | Concrete Platform Example | Protection Provided |
|---|---|---|---|
| **At Rest** | **AES-256 encryption** | The fixed `JOBS` list and sensor-processing records stored on a zone controller are encrypted on disk. | If the storage device is stolen or accessed without authorization, the stored job and sensor information cannot be easily read. |
| **In Transit** | **TLS 1.3 encryption** | A real-time public-safety alert sent from a zone controller to the Smart City Operations dashboard is transmitted over TLS 1.3. | TLS protects the alert from being intercepted or modified while travelling across the network. |
| **In Use** | **Memory protection and process isolation** | The Banker's-Algorithm safety check from the **scheduler and Banker's-Algorithm engine from Part 1** operates on resource-allocation data in system memory. | Process and memory isolation prevents unauthorized processes from directly accessing or modifying the data while the safety calculation is being performed. |

Together, IAM and data-protection controls restrict who can access the platform and protect the platform's data throughout its lifecycle: when it is stored, transmitted, and actively processed by the **scheduler and Banker's-Algorithm engine from Part 1**.

## Task 13 — IoT Connectivity and Six-Layer Architecture

### IoT Device Connectivity

The Smart City platform uses different communication technologies depending on the device's range, power requirements, and data volume.

| Sensor / Device Type | Communication Technology | Reason for Selection |
|---|---|---|
| **AI Traffic Camera / License-Plate Trigger** | **5G** | Traffic cameras can generate high-volume video and require low-latency communication. 5G provides high bandwidth and low latency, making it suitable for roadside cameras and real-time traffic or safety events. |
| **Air Quality / Environmental Sensor** | **LoRaWAN** | Environmental sensors usually send small amounts of data periodically and may operate on battery power. LoRaWAN provides long-range communication with low power consumption, making it suitable for distributed environmental sensors across the three zones. |
| **First-Responder Wearable / SOS Device** | **NB-IoT** | Wearable safety devices need reliable wide-area connectivity while consuming limited power. NB-IoT is suitable for low-bandwidth telemetry such as emergency alerts, location information, and sensor readings over cellular networks. |

### Six-Layer IoT Architecture

The platform can be mapped to the six IoT architecture layers as follows:

| IoT Architecture Layer | Smart City Platform Component |
|---|---|
| **1. Physical Environment** | Roads, traffic intersections, public facilities, environmental conditions, vehicles, and other physical assets across Zone-A, Zone-B, and Zone-C. |
| **2. Perception / Device** | Traffic cameras, air-quality sensors, environmental sensors, first-responder wearable devices, SOS buttons, and their microcontrollers/transceivers. |
| **3. Gateway** | The Zone-A, Zone-B, and Zone-C zone controllers collect sensor data, perform local processing, and act as gateways between IoT devices and the network. |
| **4. Network Communication** | 5G, LoRaWAN, NB-IoT, and secure IP networking provide communication between sensors, zone controllers, and cloud services. |
| **5. Cloud Platform** | **The scheduler and Banker's-Algorithm engine from Part 1** operates as the fixed compute core at this layer, together with the platform's data storage and messaging services. |
| **6. Application** | The central Smart City Operations Dashboard, emergency monitoring interfaces, and other municipal applications that consume the processed sensor and operational data. |

The **scheduler and Banker's-Algorithm engine from Part 1** therefore forms part of the Cloud Platform Layer, where it processes the sensor-processing jobs and performs resource-safety checks before resources are allocated.

## Task 14 — Threats and Mitigations

The Smart City platform combines IoT devices, cloud services, network communication, and the **scheduler and Banker's-Algorithm engine from Part 1**, so both IoT and cloud-security threats must be considered.

| Threat | Concrete Scenario | Specific Mitigation |
|---|---|---|
| **IoT Edge Physical Tampering** | An attacker physically accesses a Zone-B controller and attempts to extract credentials or install modified firmware. This could compromise the sensor data and the **scheduler and Banker's-Algorithm engine from Part 1** running on the controller. | Use **Secure Boot with a TPM/Secure Element** so that only digitally signed firmware can execute, and protect cryptographic keys inside the hardware security module. |
| **Cloud Resource Exhaustion / DoS** | A compromised zone device sends a large number of malicious or resource-intensive requests to the cloud services, consuming CPU and memory needed by the **scheduler and Banker's-Algorithm engine from Part 1**. | Apply **API rate limiting** and request validation at the API Gateway so excessive or malformed requests are rejected before reaching the compute engine. |
| **Man-in-the-Middle (MitM) and Replay Attack** | An attacker intercepts a public-safety alert travelling from a zone controller to the Smart City Operations platform and attempts to modify or replay the message to generate a false alert. | Use **mutual TLS (mTLS)** for authenticated encrypted communication and include timestamps/nonces in messages so old captured messages can be detected and rejected. |

These mitigations provide protection at the device, cloud, and communication levels while helping maintain the integrity and availability of the **scheduler and Banker's-Algorithm engine from Part 1**.
