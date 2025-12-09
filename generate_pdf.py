"""
Generate 10-page PDF for Insurance Claim Document
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

def generate_claim_pdf(output_path="data/insurance_claim_CLM2024001.pdf"):
    """Generate a professional 10-page insurance claim PDF"""

    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    subheader_style = ParagraphStyle(
        'CustomSubHeader',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    )

    # PAGE 1: Title and Overview
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("COMPREHENSIVE INSURANCE CLAIM REPORT", title_style))
    elements.append(Paragraph("Claim ID: CLM-2024-001", title_style))
    elements.append(Spacer(1, 0.3*inch))

    # Claim info table
    claim_data = [
        ['Document Type:', 'Multi-Vehicle Collision Claim - Complete Timeline'],
        ['Policy Number:', 'POL-2024-VEH-45782'],
        ['Claim Status:', 'Under Review'],
        ['Filing Date:', 'January 15, 2024'],
        ['Last Updated:', 'February 28, 2024'],
        ['Policyholder:', 'Sarah Mitchell'],
        ['Policy Type:', 'Comprehensive Auto Insurance'],
    ]

    claim_table = Table(claim_data, colWidths=[2*inch, 4*inch])
    claim_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(claim_table)
    elements.append(Spacer(1, 0.3*inch))

    # Section 1: Policy Information
    elements.append(Paragraph("SECTION 1: POLICY INFORMATION", header_style))

    elements.append(Paragraph("Coverage Details", subheader_style))
    coverage_text = """
    The policyholder, Sarah Mitchell, maintains a comprehensive auto insurance policy effective from
    June 1, 2023 through June 1, 2025, with an annual premium of $1,847.50. The policy provides extensive
    coverage including bodily injury liability ($250,000 per person / $500,000 per accident), property
    damage liability ($100,000 per accident), collision and comprehensive coverage at actual cash value
    minus deductible, uninsured motorist coverage ($100,000 per person / $300,000 per accident), and
    medical payments coverage ($5,000 per person).
    """
    elements.append(Paragraph(coverage_text, body_style))

    elements.append(Paragraph("Deductible Information", subheader_style))
    deductible_text = """
    <b>Collision Deductible: $750</b><br/>
    <b>Comprehensive Deductible: $500</b><br/>
    <b>Glass Deductible: $100</b> (waived for repairs)<br/><br/>

    The collision deductible of $750 applies to this claim as the incident involved a collision with
    another vehicle. This deductible amount will be subtracted from the total repair costs when
    calculating the insurance payout.
    """
    elements.append(Paragraph(deductible_text, body_style))

    elements.append(Paragraph("Insured Vehicle", subheader_style))
    vehicle_text = """
    Make/Model: 2021 Honda Accord EX<br/>
    VIN: 1HGCV1F39LA012345<br/>
    Color: Silver Metallic<br/>
    Mileage at Incident: 23,847 miles<br/>
    Estimated Value: $28,000<br/><br/>

    The insured vehicle is a well-maintained 2021 Honda Accord EX in excellent condition prior to
    the incident, with no pre-existing damage reported.
    """
    elements.append(Paragraph(vehicle_text, body_style))

    elements.append(Paragraph("Agent of Record", subheader_style))
    agent_text = """
    Michael Chen, License #INS-45892<br/>
    Premier Insurance Services<br/>
    Los Angeles, CA<br/>
    Phone: (323) 555-0100<br/>
    Email: mchen@premierinsurance.com
    """
    elements.append(Paragraph(agent_text, body_style))

    elements.append(PageBreak())

    # PAGE 2: Incident Details
    elements.append(Paragraph("SECTION 2: INCIDENT TIMELINE AND DETAILS", header_style))

    elements.append(Paragraph("Incident Overview", subheader_style))
    incident_overview = """
    On Friday, January 12, 2024, at approximately 7:42 AM, a multi-vehicle collision occurred at the
    intersection of Wilshire Boulevard and Vermont Avenue in Los Angeles, California (90005). The
    incident took place during morning rush hour under clear weather conditions with dry road surfaces
    and a temperature of 58°F. The collision involved three vehicles and resulted in significant
    property damage and minor injuries.
    """
    elements.append(Paragraph(incident_overview, body_style))

    elements.append(Paragraph("Chronological Timeline of Events", subheader_style))
    timeline_text = """
    <b>7:38 AM</b> - Claimant Sarah Mitchell departs from home at 2847 Oakwood Drive, heading to her
    workplace at 450 Corporate Center, approximately 8.3 miles away.<br/><br/>

    <b>7:41 AM</b> - Claimant traveling eastbound on Wilshire Blvd approaching Vermont Ave intersection.
    Traffic signal shows green light. Vehicle traveling at approximately 35 mph (posted speed limit
    is 35 mph).<br/><br/>

    <b>7:42:15 AM - INCIDENT OCCURS</b> - Third-party vehicle (2019 Toyota Camry driven by Robert Harrison)
    traveling southbound on Vermont Ave fails to stop at red traffic signal. Harrison's vehicle enters
    intersection at estimated 45 mph without braking. The Camry strikes Mitchell's Honda Accord on the
    driver's side door and front quarter panel with significant force. The impact causes Mitchell's
    vehicle to rotate approximately 90 degrees counterclockwise, coming to rest partially within the
    intersection.<br/><br/>

    <b>7:42:30 AM</b> - Secondary collision occurs as a fourth vehicle (2020 Ford Explorer driven by
    Jennifer Park) traveling behind Mitchell's vehicle is unable to stop in time due to the sudden
    obstruction. Park's vehicle strikes the rear bumper of Mitchell's vehicle at low speed (estimated
    10-15 mph). This secondary impact is minor compared to the primary collision.<br/><br/>

    <b>7:43 AM</b> - Robert Harrison exits his vehicle, appearing visibly disoriented and unstable.
    Multiple witnesses at the scene report a strong odor of alcohol emanating from Harrison.<br/><br/>

    <b>7:44 AM</b> - Jennifer Park places 911 call reporting a two-vehicle collision with possible
    injuries and suspected DUI driver. Emergency services are dispatched.<br/><br/>

    <b>7:47 AM</b> - LAPD Unit 15-A-32 and Fire Rescue Team 27 are dispatched to the scene.<br/><br/>

    <b>7:51 AM</b> - LAPD Officers Garcia (Badge #4782) and Thompson (Badge #5123) arrive on scene
    and begin initial assessment and traffic control.<br/><br/>

    <b>7:53 AM</b> - Fire Rescue paramedics arrive and begin medical assessment of all parties involved
    in the collision.
    """
    elements.append(Paragraph(timeline_text, body_style))

    elements.append(PageBreak())

    # PAGE 3: Incident Timeline Continued
    elements.append(Paragraph("Incident Timeline (Continued)", subheader_style))
    timeline_continued = """
    <b>7:55 AM</b> - Officer Garcia administers standardized field sobriety tests to Robert Harrison.
    Harrison fails all three tests: Horizontal Gaze Nystagmus (HGN), Walk-and-Turn, and One-Leg Stand.
    Harrison exhibits clear signs of impairment including slurred speech, bloodshot eyes, unstable gait,
    and inability to follow simple instructions.<br/><br/>

    <b>7:58 AM</b> - Sarah Mitchell reports neck pain and headache to paramedics. Given the mechanism
    of injury (side-impact collision), paramedics recommend immediate hospital evaluation for possible
    cervical strain and head injury assessment.<br/><br/>

    <b>8:02 AM</b> - Preliminary breathalyzer test administered to Harrison. Results show Blood Alcohol
    Concentration (BAC) of 0.14%, significantly exceeding the legal limit of 0.08%. Harrison is
    immediately placed under arrest for Driving Under the Influence (DUI) and reckless driving. Miranda
    rights are read at the scene.<br/><br/>

    <b>8:15 AM</b> - Mitchell transported via AMR Ambulance #427 to Cedars-Sinai Medical Center Emergency
    Department for comprehensive medical evaluation and treatment. Paramedic report indicates mechanism
    of injury consistent with whiplash-type cervical strain.<br/><br/>

    <b>8:35 AM</b> - Three tow trucks arrive at scene. Mitchell's Honda Accord towed to Premier Auto
    Body (5847 Santa Monica Blvd) per policyholder's insurance network. Harrison's Toyota Camry
    impounded to LAPD impound facility as part of DUI investigation. Park's Ford Explorer sustains
    only minor cosmetic damage and is driven from scene by owner.<br/><br/>

    <b>9:47 AM</b> - Mitchell evaluated at Cedars-Sinai Emergency Department by Dr. Amanda Foster, MD
    (Emergency Medicine). Comprehensive physical examination conducted. Cervical spine X-rays ordered
    and completed, showing no fractures or dislocations. Final diagnosis: Cervical strain (whiplash)
    and post-traumatic headache. Minor contusions noted on left shoulder consistent with seatbelt
    restraint (indicating proper seatbelt use during collision).<br/><br/>

    <b>9:47 AM - 10:17 AM</b> - Treatment provided includes soft cervical collar for support and
    comfort, pain management with ibuprofen 600mg administered orally in emergency department.
    Prescriptions provided for home use: Ibuprofen 600mg (#20 tablets) and Cyclobenzaprine 10mg
    muscle relaxant (#10 tablets).<br/><br/>

    <b>10:17 AM</b> - Mitchell discharged from emergency department in stable condition with detailed
    discharge instructions. Return precautions explained: immediate return if symptoms worsen, new
    neurological symptoms develop, or severe headache occurs. Follow-up recommended with primary care
    physician within 3-5 days.<br/><br/>

    <b>10:30 AM</b> - Mitchell's spouse, David Mitchell, arrives at hospital and transports patient home.
    """
    elements.append(Paragraph(timeline_continued, body_style))

    elements.append(PageBreak())

    # PAGE 4: Post-Incident Timeline
    elements.append(Paragraph("Post-Incident Timeline and Claim Processing", subheader_style))
    post_incident = """
    <b>January 12, 2024 - 2:15 PM</b> - Sarah Mitchell contacts Premier Insurance Services to report
    the claim. Speaks with claims representative Linda Torres who creates initial claim record. Claim
    number CLM-2024-001 is assigned. Initial information gathered includes basic incident details,
    parties involved, and police report number.<br/><br/>

    <b>January 13, 2024 - 10:00 AM</b> - Senior Claims Adjuster Kevin Park is assigned to handle the
    case. Park reviews initial claim documentation and police report summary.<br/><br/>

    <b>January 14, 2024 - 3:30 PM</b> - Adjuster Park conducts on-site vehicle inspection at Premier
    Auto Body. Comprehensive photographic documentation completed (47 photographs taken from multiple
    angles). Initial damage assessment indicates significant structural damage requiring detailed
    tear-down inspection.<br/><br/>

    <b>January 15, 2024 - 9:00 AM</b> - Formal claim officially filed with complete documentation
    package including police report, witness statements, medical records, and vehicle inspection
    report.<br/><br/>

    <b>January 15, 2024 - 11:45 AM</b> - Premier Auto Body completes initial damage estimate.
    Estimated repair cost: $12,847.50. Estimated repair time: 14-16 business days, pending parts
    availability from Honda supplier network. Estimate includes parts, labor, paint materials, and
    associated fees.<br/><br/>

    <b>January 16, 2024 - 2:00 PM</b> - Adjuster Park contacts Nationwide Insurance, the carrier for
    at-fault driver Robert Harrison (Policy #NW-2023-887654). Third-party liability investigation
    formally initiated. Nationwide assigns claim handler Jennifer Rodriguez to the case.<br/><br/>

    <b>January 18, 2024</b> - Complete police report obtained from LAPD (Report #2024-LAPD-001847).
    Report documents Harrison's citations: DUI with BAC 0.14%, failure to stop at red signal, reckless
    driving, and driving on suspended license. Report clearly establishes 100% fault with Harrison.
    Traffic signal timing verified showing proper operation. Intersection surveillance video obtained
    from nearby 7-Eleven confirms sequence of events.<br/><br/>

    <b>January 19, 2024 - 4:15 PM</b> - Rental vehicle authorized for Mitchell through Enterprise
    Rent-A-Car. 2024 Toyota Corolla provided at daily rate of $45.00. Coverage period authorized
    for up to 30 days while vehicle repairs are completed. Mitchell's policy includes rental
    reimbursement up to $50/day maximum.<br/><br/>

    <b>January 22, 2024 - 1:00 PM</b> - Mitchell attends follow-up appointment with Dr. Rachel Kim, MD
    (Orthopedic Surgery) at Westside Orthopedic Medical Group. Continued neck pain and stiffness
    reported. Physical examination reveals reduced cervical range of motion. Physical therapy prescribed:
    8 sessions over 4 weeks, twice weekly, focusing on cervical range of motion exercises, strengthening,
    and pain management modalities. Return to work authorized with restrictions: no heavy lifting over
    10 pounds, frequent position changes recommended.
    """
    elements.append(Paragraph(post_incident, body_style))

    elements.append(PageBreak())

    # PAGE 5: Claim Processing Continued
    elements.append(Paragraph("Claim Processing and Repairs", subheader_style))
    processing = """
    <b>January 24, 2024</b> - During vehicle tear-down inspection, additional hidden structural damage
    discovered that was not visible during initial assessment. Supplemental damage includes: unibody
    driver's side rocker panel displaced 12mm requiring pulling and straightening, front subframe
    mounting point showing stress requiring reinforcement, left front lower control arm bent beyond
    manufacturer specifications, steering linkage requires replacement due to impact forces.
    Supplemental estimate: additional $4,237.00. New total estimate: $17,084.50. Revised repair time:
    18-20 business days due to additional structural work required.<br/><br/>

    <b>January 26, 2024</b> - Nationwide Insurance formally accepts 100% liability for the collision
    based on clear evidence: police report establishing fault, witness statements corroborating events,
    surveillance video confirmation, Harrison's DUI arrest and citations. Nationwide agrees to cover
    all property damage costs and medical expenses. Claims handler Rodriguez confirms authorization
    for full repair costs and medical treatment.<br/><br/>

    <b>January 29, 2024</b> - Vehicle repairs formally authorized and commenced at Premier Auto Body.
    I-CAR Platinum certified technicians assigned to the repair. Parts ordered from Honda genuine
    parts supplier network. Estimated parts delivery: 5-7 business days for standard components,
    10-14 days for structural components requiring special order.<br/><br/>

    <b>February 2, 2024</b> - Mitchell begins physical therapy at Pacific Coast Physical Therapy.
    Treating therapist: Marcus Rodriguez, PT, DPT (Doctor of Physical Therapy). Initial evaluation
    completed: Cervical range of motion measured at 40° flexion (normal 50°), 45° extension (normal
    60°), 60° rotation bilateral (normal 80°), 30° lateral flexion bilateral (normal 45°). Muscle
    strength testing shows 4/5 strength throughout cervical musculature. Pain level reported as 5/10
    at rest, 7/10 with movement. Treatment plan includes manual therapy (soft tissue mobilization and
    joint mobilization), therapeutic exercises for range of motion and strengthening, postural
    correction training, and therapeutic modalities (heat, ice, electrical stimulation) as needed.
    Home exercise program provided.<br/><br/>

    <b>February 5, 2024</b> - Parts delivery delay reported. Honda door panel assembly initially ordered
    was incorrect specification due to VIN lookup error in parts system. Correct parts for 2021 Honda
    Accord EX re-ordered. Additional delay: 7-10 business days. Customer notification provided. Rental
    car coverage extended accordingly.<br/><br/>

    <b>February 5, 2024</b> - Criminal case arraignment for Robert Harrison held at Los Angeles Superior
    Court. Case Number: 24CR-001847. Charges filed: DUI with injury (felony classification due to two
    prior DUI convictions in 2016 and 2019), reckless driving causing injury. Preliminary hearing
    scheduled for March 15, 2024. Harrison remains released on $50,000 bail with conditions including
    ignition interlock device requirement, alcohol monitoring, and license suspension.<br/><br/>

    <b>February 12, 2024</b> - Correct replacement parts received at Premier Auto Body. Vehicle repairs
    resume with full parts inventory available. Structural repairs completed first, followed by
    component replacement, then body work and paint preparation.
    """
    elements.append(Paragraph(processing, body_style))

    elements.append(PageBreak())

    # PAGE 6: Witness Statements
    elements.append(Paragraph("SECTION 3: WITNESS STATEMENTS", header_style))

    elements.append(Paragraph("Witness #1: Marcus Thompson", subheader_style))
    witness1 = """
    Address: 847 S. Vermont Ave, Apt 402, Los Angeles, CA 90005<br/>
    Phone: (213) 555-0147<br/>
    Statement Date: January 12, 2024, 8:10 AM<br/><br/>

    "I was standing at the bus stop on the northeast corner of Wilshire and Vermont waiting for the
    720 Rapid bus. I had a completely clear, unobstructed view of the entire intersection. I saw the
    silver Honda coming eastbound on Wilshire with the green traffic light. The driver appeared to be
    traveling at normal speed, probably around 35 mph, which is the speed limit. Then this white Camry
    came speeding down Vermont going really fast, had to be going at least 45, maybe even 50 mph. The
    Camry never even touched his brakes - not even a tap. The red light was clearly visible and had been
    red for at least 2-3 seconds before he entered the intersection. He just blew right through it and
    T-boned that Honda extremely hard on the driver's side. The impact was so violent that the Honda
    spun around like a top, probably did a complete 90-degree spin. Then the SUV that was behind the
    Honda couldn't stop fast enough and hit the Honda from behind, but that second hit was just a tap
    compared to the first massive impact. The guy who ran the red light got out of his car and he was
    stumbling all over the place, could barely stand up straight. I could smell alcohol from where I
    was standing, and I was like 30 feet away from him. The smell was that strong. He was definitely
    drunk - no question about it. The woman in the Honda looked really shaken up when they helped her
    out of the car. The whole thing was 100% the Camry driver's fault. He ran a clearly red light while
    driving under the influence."
    """
    elements.append(Paragraph(witness1, body_style))

    elements.append(Paragraph("Witness #2: Elena Rodriguez", subheader_style))
    witness2 = """
    Address: 5632 Wilshire Blvd, Suite 900, Los Angeles, CA 90036<br/>
    Phone: (323) 555-0293<br/>
    Statement Date: January 12, 2024, 8:25 AM<br/><br/>

    "I was driving westbound on Wilshire in the left turn lane, stopped and waiting to make a left turn
    onto Vermont. I had a red light and was completely stopped at the intersection. The Honda going
    through the intersection had a solid green light - there's absolutely no question about that. I saw
    everything happen right in front of me. The Camry driver had a red light, and it had been red for
    several seconds before he entered the intersection. He wasn't even slowing down - he was actually
    accelerating or maintaining high speed. The collision was absolutely terrible. He hit the Honda
    directly on the driver's door at full speed. The sound of the impact was incredibly loud. Then I
    saw another car hit the Honda from behind. I immediately thought the Honda driver must be seriously
    hurt because of where the impact was on the driver's side. The Camry driver got out and it was
    immediately obvious he was intoxicated - he could barely stand up straight, was swaying, and seemed
    completely out of it. I gave all my contact information to Officer Garcia at the scene. The Camry
    driver is 100% at fault. He ran a very, very red light while clearly driving drunk."
    """
    elements.append(Paragraph(witness2, body_style))

    elements.append(PageBreak())

    # PAGE 7: Additional Witness and Medical Documentation
    elements.append(Paragraph("Witness #4: Patricia O'Brien (Registered Nurse)", subheader_style))
    witness4 = """
    Address: 1423 S. Vermont Ave, Los Angeles, CA 90006<br/>
    Phone: (213) 555-0734<br/>
    Occupation: Registered Nurse, USC Medical Center<br/>
    Statement Date: January 14, 2024, 11:45 AM (Follow-up detailed statement)<br/><br/>

    "I was jogging northbound on Vermont approaching Wilshire. I was on the east sidewalk approximately
    half a block south of the intersection when I heard the sound of tires screeching followed immediately
    by an extremely loud crash. I looked up instantly and saw that the collision had just occurred. The
    white Camry had just impacted the silver Honda. I'm a registered nurse at USC Medical Center with
    12 years of emergency department experience, so I immediately ran up to the scene to see if anyone
    needed medical help before paramedics could arrive. The woman in the Honda seemed dazed but conscious.
    The man from the Camry got out and was definitely, without question, intoxicated. As a medical
    professional, I can recognize the signs: severely slurred speech, inability to walk in a straight
    line, extremely bloodshot and watery eyes, and a very strong odor of alcohol. I stayed at the scene
    until paramedics arrived to make sure the woman in the Honda was stabilized. One detail I specifically
    remember and mentioned to the police officer - the street lights were still on their normal
    operational cycle. The sun had risen at 6:58 AM that morning, and it was 7:42 AM when this happened,
    so there was full daylight. The traffic signals were clearly visible with excellent visibility.
    There is absolutely no way the Camry driver could have missed seeing the red light - he just chose
    to run it while driving drunk. Also, I noticed when I walked past the Camry that there was one of
    those pine tree air fresheners hanging from the rearview mirror that said 'Pine Forest' on it, but
    the car absolutely reeked of vodka. It seemed like he was trying to mask the alcohol smell but it
    didn't work at all. I provided all this information to the police officer."
    """
    elements.append(Paragraph(witness4, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("SECTION 4: MEDICAL DOCUMENTATION SUMMARY", header_style))

    elements.append(Paragraph("Emergency Department Treatment", subheader_style))
    medical1 = """
    <b>Facility:</b> Cedars-Sinai Medical Center, Emergency Department<br/>
    <b>Date:</b> January 12, 2024 (8:35 AM - 10:17 AM)<br/>
    <b>Treating Physician:</b> Dr. Amanda Foster, MD (Emergency Medicine)<br/>
    <b>Chief Complaint:</b> Neck pain and headache following motor vehicle collision<br/><br/>

    <b>Diagnosis:</b> (1) Cervical strain (whiplash) secondary to motor vehicle collision,
    (2) Post-traumatic headache, (3) Minor contusions<br/><br/>

    <b>Treatment Provided:</b> Soft cervical collar for support and comfort, Ibuprofen 600mg administered
    orally in ED, prescriptions provided for home use: Ibuprofen 600mg (#20 tablets) every 6 hours as
    needed for pain, Cyclobenzaprine 10mg (#10 tablets) at bedtime as needed for muscle spasm<br/><br/>

    <b>Imaging:</b> Cervical spine X-ray (3 views) - No fracture or dislocation identified, normal
    alignment, no prevertebral soft tissue swelling<br/><br/>

    <b>Disposition:</b> Discharged home in stable condition with spouse. Follow-up with primary care
    physician in 3-5 days. Return precautions explained.<br/><br/>

    <b>Medical Charges:</b> $2,847.00
    """
    elements.append(Paragraph(medical1, body_style))

    elements.append(PageBreak())

    # PAGE 8: Medical Documentation Continued and Vehicle Damage
    elements.append(Paragraph("Orthopedic Follow-Up and Physical Therapy", subheader_style))
    medical2 = """
    <b>Orthopedic Consultation</b><br/>
    Facility: Westside Orthopedic Medical Group<br/>
    Date: January 22, 2024<br/>
    Physician: Dr. Rachel Kim, MD (Orthopedic Surgery)<br/>
    Assessment: Cervical strain with ongoing symptoms, improving but not fully resolved<br/>
    Plan: Physical therapy prescribed - 8 sessions over 4 weeks, cleared for return to work with
    restrictions (no heavy lifting >10 lbs), follow-up in 4 weeks<br/>
    Charges: $387.00<br/><br/>

    <b>Physical Therapy Treatment Course</b><br/>
    Facility: Pacific Coast Physical Therapy<br/>
    Treating Therapist: Marcus Rodriguez, PT, DPT<br/>
    Duration: February 2, 2024 - February 27, 2024<br/>
    Total Sessions: 8 sessions (2x per week for 4 weeks)<br/><br/>

    Progress Summary: Patient made excellent progress throughout treatment course. Pain reduced from
    initial 5/10 at rest to 1/10 by discharge. Cervical range of motion improved from significantly
    restricted to 90% of normal values. Strength improved from 4/5 to 5/5 throughout. Patient independent
    with home exercise program. Cleared for all regular activities at discharge. May experience occasional
    stiffness which should resolve within 2-4 weeks. No further therapy needed at this time.<br/><br/>

    Charges: $1,400.00 (8 sessions @ $175 per session)
    """
    elements.append(Paragraph(medical2, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("SECTION 5: VEHICLE DAMAGE ASSESSMENT", header_style))

    elements.append(Paragraph("Initial Damage Inspection", subheader_style))
    damage1 = """
    <b>Inspector:</b> Kevin Park, Senior Claims Adjuster<br/>
    <b>Date:</b> January 14, 2024<br/>
    <b>Location:</b> Premier Auto Body, 5847 Santa Monica Blvd, Los Angeles, CA<br/>
    <b>Vehicle:</b> 2021 Honda Accord EX, VIN 1HGCV1F39LA012345, Mileage: 23,847<br/><br/>

    <b>Primary Damage (Driver's Side):</b> Front door severely crushed inward approximately 8 inches at
    point of impact, door frame bent preventing door operation, side curtain airbag deployed, front door
    window completely shattered, driver's side front fender pushed back approximately 3 inches, A-pillar
    shows stress marks but no structural failure, side mirror housing cracked with mirror intact<br/><br/>

    <b>Secondary Damage (Rear):</b> Rear bumper cover cracked and pushed in approximately 2 inches at
    center, rear bumper reinforcement bar bent, taillight housings intact, trunk lid alignment off by
    0.5 inches<br/><br/>

    <b>Safety Systems:</b> Driver's side curtain airbag deployed, driver's seat-mounted side airbag
    deployed, front driver airbag did NOT deploy (appropriate for side impact), all SRS components
    require replacement per manufacturer specifications<br/><br/>

    <b>Initial Repair Estimate:</b><br/>
    Parts: $6,112.00<br/>
    Labor: 36.5 hours @ $125/hour = $4,562.50<br/>
    Paint and Materials: $1,473.00<br/>
    Sales Tax (9.5%): $580.00<br/>
    <b>Initial Total: $12,847.50</b><br/>
    Estimated Repair Time: 14-16 business days
    """
    elements.append(Paragraph(damage1, body_style))

    elements.append(PageBreak())

    # PAGE 9: Final Repair Documentation and Financial Summary
    elements.append(Paragraph("Supplemental Damage and Final Repair", subheader_style))
    damage2 = """
    <b>Supplemental Estimate Date:</b> January 24, 2024<br/><br/>

    <b>Additional Hidden Damage Discovered:</b><br/>
    • Unibody driver's side rocker panel displaced 12mm, requires pulling and straightening: $1,247.00
    (labor 6.5 hours)<br/>
    • Front subframe mounting point shows stress, requires reinforcement: $834.00 (labor 4.0 hours)<br/>
    • Left front lower control arm bent beyond specification: $387.00 + labor 2.5 hours ($312.50)<br/>
    • Wheel alignment required after suspension repair: $179.00<br/>
    • Steering linkage replacement due to impact forces: $521.00 + labor 3.0 hours ($375.00)<br/><br/>

    <b>Supplemental Total: $4,237.00</b><br/>
    <b>Revised Total Estimate: $17,084.50</b><br/>
    Revised Repair Time: 18-20 business days<br/><br/>

    <b>Final Repair Invoice</b><br/>
    Completion Date: February 15, 2024<br/>
    Actual Repair Time: 19 business days<br/><br/>

    Parts Total: $6,499.00<br/>
    Labor Total: $6,125.00 (49 hours @ $125/hour)<br/>
    Paint & Materials: $1,612.00<br/>
    Sublet Services (alignment, calibration): $478.00<br/>
    Subtotal: $14,714.00<br/>
    Sales Tax: $1,397.83<br/>
    <b>Final Total: $17,111.83</b><br/><br/>

    <b>Quality Inspection:</b> PASSED<br/>
    Inspector: Robert Martinez (I-CAR Platinum Certified)<br/>
    Date: February 15, 2024<br/>
    Vehicle restored to pre-loss condition. All repairs meet or exceed manufacturer specifications.
    All safety systems tested and operational. ADAS (Advanced Driver Assistance Systems) calibration
    completed successfully. Vehicle ready for customer pickup.
    """
    elements.append(Paragraph(damage2, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("SECTION 6: FINANCIAL SUMMARY", header_style))
    financial = """
    <b>Total Claim Costs:</b><br/><br/>

    Vehicle Repair: $17,111.83<br/>
    Rental Car (28 days @ $45/day + tax): $1,402.47<br/>
    Emergency Department Visit: $2,847.00<br/>
    Orthopedic Consultation: $387.00<br/>
    Physical Therapy (8 sessions): $1,400.00<br/>
    Prescriptions: $47.50<br/>
    Towing: $175.00<br/><br/>

    <b>TOTAL CLAIM AMOUNT: $23,370.80</b><br/><br/>

    <b>Payment Responsibility:</b><br/><br/>

    Claimant's Collision Deductible: $750.00<br/>
    (Applied to vehicle repair cost)<br/><br/>

    Third-Party Liability (Nationwide Insurance for Robert Harrison):<br/>
    • Vehicle Repair (after deductible): $16,361.83<br/>
    • Rental Car: $1,402.47<br/>
    • All Medical Expenses: $4,681.50<br/>
    • Towing: $175.00<br/>
    <b>Third-Party Total: $22,620.80</b><br/><br/>

    <b>Subrogation Status:</b><br/>
    Date Initiated: January 26, 2024<br/>
    Third-Party Carrier: Nationwide Insurance<br/>
    Claim Number (Nationwide): NW-CLM-2024-009847<br/>
    Liability Accepted: Yes, 100% accepted January 26, 2024<br/>
    Recovery Amount Sought: $22,620.80<br/>
    Status as of February 28, 2024: Payment pending, expected by March 15, 2024<br/><br/>

    Policyholder deductible reimbursement of $750.00 expected upon completion of subrogation recovery.
    """
    elements.append(Paragraph(financial, body_style))

    elements.append(PageBreak())

    # PAGE 10: Conclusion and Case Notes
    elements.append(Paragraph("SECTION 7: CASE NOTES AND CONCLUSION", header_style))

    elements.append(Paragraph("Claims Adjuster Assessment", subheader_style))
    adjuster_notes = """
    <b>Claims Adjuster:</b> Kevin Park, Senior Claims Adjuster<br/>
    <b>Date:</b> February 28, 2024<br/><br/>

    This claim presents a textbook clear liability case with an intoxicated driver running a red traffic
    signal. The evidence supporting our policyholder's account is overwhelming and irrefutable:<br/><br/>

    • Police report clearly establishes 100% fault with at-fault driver Harrison<br/>
    • Harrison arrested at scene with BAC 0.14% (1.75x legal limit)<br/>
    • Four independent credible witnesses, including a registered nurse<br/>
    • Intersection surveillance video confirms sequence of events<br/>
    • Traffic signal timing verification shows proper operation<br/>
    • At-fault driver has two prior DUI convictions (2016, 2019)<br/>
    • At-fault driver was driving on suspended license at time of collision<br/><br/>

    Vehicle damage assessment was thorough and appropriate. Initial estimate of $12,847.50 was reasonable
    based on visible damage. The supplemental estimate of $4,237.00 bringing total to $17,084.50 is
    consistent with industry standards for side-impact collisions where hidden structural damage is
    commonly discovered during tear-down inspection. Final repair cost of $17,111.83 is within acceptable
    variance of the revised estimate (difference of $27.33 or 0.16%).<br/><br/>

    Vehicle damage represents approximately 61% of the vehicle's pre-loss value ($28,000), well below
    the 75% total loss threshold. The decision to repair rather than declare total loss was appropriate
    and in the policyholder's best interest.<br/><br/>

    Medical treatment received by the policyholder is entirely reasonable, appropriate, and directly
    related to the collision mechanism. Cervical strain (whiplash) is the expected and most common injury
    pattern from side-impact T-bone collisions. The treatment course - emergency department evaluation,
    orthopedic follow-up, and physical therapy - represents standard of care for this injury type.
    Physical therapy prescription of 8 sessions over 4 weeks is conservative and appropriate. Medical
    expenses totaling $4,681.50 are reasonable and customary for the Los Angeles area.<br/><br/>

    Rental vehicle duration of 28 days is reasonable given the repair complexity and parts delays
    (incorrect parts initially ordered requiring re-order). Rental rate of $45/day for comparable vehicle
    (Toyota Corolla) is within policy limits and market rate.<br/><br/>

    Nationwide Insurance has been professional and cooperative throughout the claims process. Their
    acceptance of 100% liability on January 26, 2024 (only 14 days after incident) demonstrates
    recognition of the clear fault. We anticipate full recovery of all costs advanced through
    subrogation process.<br/><br/>

    The policyholder, Sarah Mitchell, has been professional, cooperative, and patient throughout the
    entire claims process. No concerns regarding claim validity or cooperation. Policyholder expressed
    satisfaction with claims handling and repair quality.<br/><br/>

    <b>Recommendation:</b> Approve claim for closure pending final subrogation payment receipt.
    All required documentation obtained and verified. Quality standards met. Customer satisfaction
    achieved.
    """
    elements.append(Paragraph(adjuster_notes, body_style))

    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("File Status and Closure Information", subheader_style))
    closure = """
    <b>Claim Status:</b> Under Final Review (as of February 28, 2024)<br/><br/>

    <b>Pending Items:</b><br/>
    1. Subrogation payment from Nationwide Insurance - Expected by March 15, 2024<br/>
    2. Deductible reimbursement to Sarah Mitchell - Upon receipt of subrogation payment<br/>
    3. Final medical bills verification - All received and processed ✓<br/>
    4. File quality review - COMPLETED February 28, 2024 ✓<br/><br/>

    <b>Anticipated Closure Date:</b> March 20, 2024<br/><br/>

    <b>File Retention:</b> Retain file per standard retention policy - 7 years from closure date<br/><br/>

    <b>Report Compiled By:</b> Kevin Park, Senior Claims Adjuster<br/>
    <b>Report Reviewed By:</b> Sandra Phillips, Claims Manager<br/>
    <b>Final Report Date:</b> February 28, 2024<br/><br/>

    <b>Confidentiality Notice:</b> This document contains confidential and proprietary information of
    Premier Insurance Services. Unauthorized disclosure or distribution is prohibited.
    """
    elements.append(Paragraph(closure, body_style))

    # Build PDF
    doc.build(elements)
    print(f"✅ PDF generated successfully: {output_path}")
    print(f"📄 Document contains 10 pages with comprehensive timeline and case details")

if __name__ == "__main__":
    generate_claim_pdf()
