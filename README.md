gbnews_network_project/
│
├── app.py                     
├── README.md                
│
├── data/                      
│   ├── database.json
│   ├── users.json            
│   ├── services_development.json
│   └── services_production.json
│
├── routes/                   
│   ├── __init__.py
│   ├── pages/                 
│   │   ├── __init__.py
│   │   ├── inventory.py
│   │   ├── it_backup.py
│   │   ├── it_continuity.py
│   │   ├── it_decision.py
│   │   ├── it_development.py
│   │   ├── it_improvement.py
│   │   └── it_production.py
│   └── users/            
│       ├── __init__.py
│       ├── login.py
│       └── register.py
│
├── scripts/                 
│   ├── __init__.py
│   └── generate_devices_json.py
│
├── static/                
│   ├── css/
│   │   └── style.css
        └── auth.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── (image files...)
│
├── templates/               
│   ├── base.html
│   ├── footer.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── sections/
│       ├── inventory.html
│       ├── it-backup.html
│       ├── it-continuity.html
│       ├── it-decision.html
│       ├── it-development.html
│       ├── it-improvement.html
│       └── it-production.html
