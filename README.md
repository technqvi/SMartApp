# About
Centralized IT service management system  to handle incident management and preventive maintenance operation process , there are serveral sub system as belows.
* [IT Service Management System)](https://github.com/technqvi/SMartApp)
* [Incident Knowledge Base & Agent Powered By Amazone Bedrock](https://github.com/technqvi/aws-bedrock-gen-ai-project?tab=readme-ov-file#incident-knownledge-base)
* [Incident Enterprise Search and Incident Summarization Powered By Google Search Vertex AI](https://github.com/technqvi/SMartSearch-Summarization)
* [Smart Analytics Data Warehouse on BigQuery](https://github.com/technqvi/SMartDataHub-DBToBigQuery)
* [Severity Level Prediction (Critical/Normal)](https://github.com/technqvi/SMart-AI/tree/main/Model-TF_DF)

### SMartApp System  consists of 2 core functions.
<img width="750" alt="image" src="https://github.com/technqvi/SMartApp/assets/38780060/a7c06417-2e6a-489b-be2f-574b852c967c">
<img width="725" alt="image" src="https://github.com/technqvi/SMartApp/assets/38780060/a5875f1a-040a-4947-9546-4b028eba543b">

 ### SMart DashBoard Asset & Incident
![image](https://github.com/technqvi/SMartApp/assets/38780060/a095f115-0c59-4ab1-9c0c-af14bc964d21)

### SMartApp Process Overview.
![SMartApp-Process](https://github.com/technqvi/SMartApp/assets/38780060/f0dd75cf-01e3-4054-8225-a8a6e4a4e151)

### Incident System
* Customer will issue incident case to Site-Manager who is in charge of.
* Site manager will assign Engineer to fix any error/problem of such an inventory.
* Site manager will track the incident based on incident type and severity level (Critical,Major,Minor and Cosmatic)   by taking note of incident details to handle  any incident cases and update incident  status.
* Site-Manager need to wait for the customer to accept the solution the engineer team  resolves  the incident's problem .
### Preventive Maintenance System
* The manager and Officer will create the MA-Plan of any project as a contract agreement. Once created MA-plan successfully,the system will copy all inventories of project for the MA-Plan.
* The system allows the manager to remove undesirable inventory items from PM Plan.
* The engineer can access to application to update any PM-Operation progress of each inventory.


## Tool and Framework
- Database: Postqresql 12
- Web Application :Python Django 3.2
- Web Server : IIS 
- Dashboard: Power BI.

## SubSystem
 - Project Management
 - Inventory Management
 - Incident Management
 - Preventive Maintenance Management
 - Model Import
 - Site Metadata Management (Branch,Data Center,Customer Support,Procut Suport)
 - Report And Dashboard
   - Advance Pivot Excel Report (Excel)
   - Site Grade Report (Excel)
   - SMartDashboard-Report For Site-Manager (PowerBI)
   - SMartBI For Customer (PowerBI)
 - [SMartApp_ScriptDev](https://github.com/technqvi/SMartApp_ScriptDev)
   
