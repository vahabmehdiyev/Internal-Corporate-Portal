# Internal Corporate Portal (IntraCorp) Backend

**Description:**  
Backend system for a corporate internal portal with IP-based authentication. Provides access to documents, FAQs, graphs and reports, news (via WebSocket), phone directory, and user management. Only accessible from allowed IP addresses within the local network.

## Features
- IP-based authentication for internal network users
- Document management (`docs`)
- FAQ section
- Graphs and reports
- Real-time news updates via WebSocket
- Phone directory (`phones`)
- User management

## Tech Stack
- Python / Flask
- WebSocket for news updates
- SQLAlchemy for database access
- REST API endpoints

## Installation
1. Clone the repository:
```bash
git clone https://github.com/<username>/internal-corp-portal.git
cd internal-corp-portal
