# About
 SMartApp System  consists of 2 sub system.
### Incident System
* Customer will issue incident case to Site-Manager who is in charge of .
* Site manager will assign Engineer to fix any error/problem of such an inventory.
* Site manager will track the incident based on incident type and severity level (Critical,Major,Minor and Cosmatic)   by taking note of incident detail to handle  any incident cases and update incident  status.
* Site-Manager need to wait for customer to accept already fixed problem to complete case.
### Preventive Maintenance System
* Site-Manager and Officer will create MA-Plan of any project as contract agreement. Once created MA-plan successfully ,the system will copy all inventories of project for the MA-Plan.
* The system allows Site-Manager to remove undesirable inventory items from PM Plan.
* Engineer is allowed to update maintenance detail of each inventory after finished MA-Operation.

### The figure below shows  SMartApp System Overview.
![image](https://github.com/technqvi/SMartApp/assets/38780060/5b8473cc-6ae2-4576-b82e-a64a3338a834)

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
 - Machine Learing Prediction (Preview)
   - Post-Severity Level Prediction (Critical/Normal) and (Critical/Major/Minor/Costmetic)
   - Daily Incident Forecast Over the next 5 days
 - [SMartApp_ScriptDev](https://github.com/technqvi/SMartApp_ScriptDev)
   