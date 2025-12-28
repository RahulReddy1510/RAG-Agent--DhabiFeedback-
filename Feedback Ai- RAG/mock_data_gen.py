import pandas as pd
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

DATA_DIR = "dhabifeedback-ai/data"
POLICIES_DIR = f"{DATA_DIR}/policies"

def generate_feedback_csv():
    data = [
        {"id": 1, "complaint": "Heavy traffic on Sheikh Zayed Road during rush hour near Marina exit", "category": "traffic", "location": "Dubai", "language": "en", "date": "2025-12-01"},
        {"id": 2, "complaint": "فاتورة كهرباء مرتفعة جداً هذا الشهر في منطقة الخالدية", "category": "utilities", "location": "Abu Dhabi", "language": "ar", "date": "2025-12-02"},
        {"id": 3, "complaint": "Water leak in Al Barsha 2 villa compound street 14", "category": "utilities", "location": "Dubai", "language": "en", "date": "2025-12-03"},
        {"id": 4, "complaint": "Need more metro feeder buses in Discovery Gardens", "category": "transport", "location": "Dubai", "language": "en", "date": "2025-12-04"},
        {"id": 5, "complaint": "تأخير في تجديد رخصة القيادة عبر التطبيق الذكي", "category": "services", "location": "Dubai", "language": "ar", "date": "2025-12-05"},
        {"id": 6, "complaint": "Street lights not working in Khalifa City A sector 12", "category": "infrastructure", "location": "Abu Dhabi", "language": "en", "date": "2025-12-06"},
        {"id": 7, "complaint": "Garbage collection missed for 3 days in JVC", "category": "sanitation", "location": "Dubai", "language": "en", "date": "2025-12-07"},
        {"id": 8, "complaint": "إزعاج من أعمال البناء في وقت متأخر من الليل في منطقة النهدة", "category": "noise", "location": "Dubai", "language": "ar", "date": "2025-12-08"},
        {"id": 9, "complaint": "Potholes on Hessa Street damaging cars", "category": "roads", "location": "Dubai", "language": "en", "date": "2025-12-09"},
        {"id": 10, "complaint": "عدم توفر مواقف سيارات كافية أمام مركز إسعاد المتعاملين في الكفاف", "category": "parking", "location": "Dubai", "language": "ar", "date": "2025-12-10"}
    ]
    # Add more rows to reach ~50 for sample
    for i in range(11, 60):
        data.append({
            "id": i, 
            "complaint": f"Sample complaint {i} about generic city services", 
            "category": "general", 
            "location": "Dubai", 
            "language": "en", 
            "date": "2025-12-11"
        })

    df = pd.DataFrame(data)
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(f"{DATA_DIR}/feedback_sample.csv", index=False)
    print(f"Generated {len(df)} feedback records.")

def create_pdf(filename, content):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    y = 750
    for line in content.split('\n'):
        if y < 50:
            c.showPage()
            y = 750
        c.drawString(40, y, line)
        y -= 20
    c.save()

def generate_policies():
    os.makedirs(POLICIES_DIR, exist_ok=True)
    
    rta_policy = """
    DUBAI ROADS AND TRANSPORT AUTHORITY (RTA) - TRAFFIC MANAGEMENT POLICY 2025
    
    1. Traffic Congestion Management
       - Heavy traffic on major highways like Sheikh Zayed Road is monitored 24/7.
       - Immediate response teams are dispatched for accidents blocking lanes.
       - Smart signals adjust timing based on traffic flow density.
    
    2. Public Transport Feeder Services
       - Feeder buses must operate with a frequency of at least every 15 minutes during peak hours.
       - Requests for new routes in areas like Discovery Gardens or JVC are reviewed quarterly.
    
    3. Parking Regulations
       - Paid parking zones operate from 8 AM to 10 PM, Monday to Saturday.
       - Unauthorized parking in reserved slots results in a fine of AED 500.
       - Customer Happiness Centers must utilize smart parking sensors.
    
    4. Road Maintenance
       - Potholes reported on main roads (e.g., Hessa St) must be repaired within 48 hours.
       - Construction noise permits are valid only between 7 AM and 8 PM. Night work requires special exemption.
    """
    
    dewa_policy = """
    DUBAI ELECTRICITY AND WATER AUTHORITY (DEWA) - CUSTOMER GUIDELINES 2025
    
    1. Bill Disputes
       - High bill complaints will instigate a smart meter check within 3 working days.
       - If a leak is suspected, the customer is responsible for internal connections (after the meter).
       - Tariff slabs: 0-2000 kWh (Green), 2000+ kWh (Red).
    
    2. Service Interruption
       - Planned maintenance requires 24-hour advance SMS notification.
       - Emergency water functioning interruptions must be resolved within 4 hours.
    
    3. Villa Compounds (e.g., Al Barsha, Springs)
       - Internal leaks in private compounds are the owner's responsibility.
       - DEWA provides list of approved maintenance contractors.
    """
    
    muni_policy = """
    DUBAI MUNICIPALITY - PUBLIC HEALTH & SANITATION RULES
    
    1. Waste Management
       - Daily collection in residential areas.
       - Missed collections reported via 800900 are addressed within 12 hours.
    
    2. Construction Noise
       - Noise levels must not exceed 55 decibels in residential areas at night.
       - Violations can be reported via the Dubai Now app 24/7.
       
    3. Public Parks
       - BBQ is only allowed in designated areas.
       - Dogs must be leashed at all times in pet-friendly zones.
    """
    
    create_pdf(f"{POLICIES_DIR}/RTA_Traffic_Policy.pdf", rta_policy)
    create_pdf(f"{POLICIES_DIR}/DEWA_Guidelines.pdf", dewa_policy)
    create_pdf(f"{POLICIES_DIR}/Dubai_Municipality_Rules.pdf", muni_policy)
    print("Generated 3 policy PDFs.")

if __name__ == "__main__":
    generate_feedback_csv()
    generate_policies()
