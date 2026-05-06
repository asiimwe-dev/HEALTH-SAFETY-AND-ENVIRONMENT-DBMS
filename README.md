# Health, Safety, and Environment (HSE) DBMS
## Project: Uganda Oil & Gas Sector

### 1. Project Overview
This database system is designed for a class project focusing on the Health, Safety, and Environment (HSE) management within Uganda's burgeoning Oil and Gas sector. It specifically targets operations in the Albertine Graben (Tilenga and Kingfisher projects) and the East African Crude Oil Pipeline (EACOP).

The system allows HSE officers to track:
- Personnel and Local Content (PAU compliance)
- Safety Incidents (LTI, Near Misses, Spills)
- Environmental Monitoring (NEMA compliance)
- Safety Training and Certifications (OPITO standards)

### 2. Database Structure
The system consists of 7 primary tables designed to capture the lifecycle of safety and environmental data:
1. **sites**: Locations of oil field operations.
2. **employees**: Workforce tracking (Operators vs. Contractors).
3. **incidents**: Detailed logs of safety events.
4. **training_courses**: Catalog of mandatory safety certifications.
5. **training_records**: Link between employees and their certificates.
6. **environmental_metrics**: Air, noise, and water quality logs.
7. **waste_management**: Hazardous waste disposal tracking.

### 3. Setup Instructions
To implement this system in a local MySQL environment:

1. **Create the Database:**
   ```sql
   CREATE DATABASE hse_db_uganda;
   USE hse_db_uganda;
   ```

2. **Run the Schema Script:**
   Import `sql/schema.sql` to create all tables and views. This includes data validation constraints.

3. **Load Sample Data:**
   Import `sql/data.sql` to populate the system with realistic data for the Tilenga and Kingfisher sites.

4. **Execute Queries:**
   Use the scripts in `sql/queries.sql` to generate reports on safety performance and environmental compliance.

### 4. Key Business Case Findings
- **Application Domain:** Upstream (Drilling) and Midstream (Pipeline).
- **Benefits:** Prevents regulatory fines from NEMA and improves safety culture.
- **Costs:** Implementation of servers and rugged devices for field workers.
- **Risks:** Remote site connectivity and data entry accuracy.

### 5. Sample Outputs
The system provides several key reports:
- **LTI Summary:** Count of Lost Time Injuries per site.
- **Training Gap Analysis:** Identification of personnel with expired safety certs.
- **Environmental Breach Log:** Highlighting sites exceeding noise or emission limits.

### 6. File Directory
- `reports/HSE_DBMS_Report.docx`: Full 10+ page project report.
- `sql/schema.sql`: Database table structures.
- `sql/data.sql`:   Sample data.
- `sql/queries.sql`: Practical SQL queries for the assignment.

---
**Course:** Database Systems
**Sector Focus:** Oil and Gas (Uganda)
**Name:** Asiimwe Gilbert
