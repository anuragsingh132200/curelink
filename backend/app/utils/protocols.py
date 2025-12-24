"""Medical protocols and knowledge base for common health conditions"""

MEDICAL_PROTOCOLS = {
    "fever": {
        "keywords": ["fever", "temperature", "hot", "burning up", "chills", "feverish"],
        "protocol": """
**Fever Management Protocol:**

1. **Assessment:**
   - Temperature reading (normal: 97-99°F/36-37°C)
   - High fever: >103°F (39.4°C) - seek immediate medical attention
   - Duration of fever

2. **Home Care (for mild fever <102°F):**
   - Rest adequately
   - Stay hydrated (water, clear fluids)
   - Light, comfortable clothing
   - Lukewarm sponge bath (avoid cold water)
   - Acetaminophen or ibuprofen (follow dosage instructions)

3. **Seek Medical Help if:**
   - Fever >103°F (39.4°C)
   - Lasting more than 3 days
   - Accompanied by severe headache, rash, difficulty breathing
   - In infants under 3 months
   - Signs of dehydration

4. **Monitor:** Track temperature every 4-6 hours
        """
    },
    "stomach_ache": {
        "keywords": ["stomach ache", "stomach pain", "abdominal pain", "belly pain", "tummy ache", "cramps", "nausea"],
        "protocol": """
**Stomach Ache Management Protocol:**

1. **Assessment:**
   - Location and type of pain (sharp, dull, cramping)
   - Duration and severity
   - Associated symptoms (nausea, vomiting, diarrhea)

2. **Home Care (for mild cases):**
   - Rest and avoid solid foods initially
   - Small sips of clear fluids (water, clear broth)
   - BRAT diet when tolerated (Bananas, Rice, Applesauce, Toast)
   - Avoid spicy, fatty, or acidic foods
   - Apply warm compress to abdomen
   - Avoid lying flat immediately after eating

3. **Seek Medical Help if:**
   - Severe or worsening pain
   - Pain lasting >24 hours
   - Bloody or black stools
   - Persistent vomiting
   - Signs of dehydration
   - Fever >101°F (38.3°C)
   - Abdominal rigidity or tenderness

4. **Avoid:** NSAIDs on empty stomach, which can worsen symptoms
        """
    },
    "headache": {
        "keywords": ["headache", "head pain", "migraine", "head hurts", "throbbing head"],
        "protocol": """
**Headache Management Protocol:**

1. **Assessment:**
   - Type: tension, migraine, cluster, sinus
   - Location and intensity (scale 1-10)
   - Triggers (stress, food, sleep, screen time)

2. **Home Care:**
   - Rest in quiet, dark room
   - Cold/warm compress on forehead or neck
   - Stay hydrated
   - Gentle neck and shoulder stretches
   - Over-the-counter pain relievers (ibuprofen, acetaminophen)
   - Avoid screens and bright lights
   - Regular sleep schedule

3. **Prevention:**
   - Identify and avoid triggers
   - Manage stress
   - Regular exercise
   - Adequate sleep (7-9 hours)
   - Stay hydrated throughout day

4. **Seek Medical Help if:**
   - Sudden severe headache ("worst headache ever")
   - Headache with fever, stiff neck, confusion
   - After head injury
   - Vision changes, weakness, or numbness
   - Headaches increasing in frequency/severity
        """
    },
    "cold_flu": {
        "keywords": ["cold", "flu", "cough", "sneeze", "runny nose", "congestion", "sore throat"],
        "protocol": """
**Cold & Flu Management Protocol:**

1. **Assessment:**
   - Symptoms: congestion, cough, sore throat, body aches
   - Fever presence and severity
   - Duration of symptoms

2. **Home Care:**
   - Rest (7-9 hours of sleep)
   - Increase fluid intake (water, warm tea, soup)
   - Gargle with salt water for sore throat
   - Use humidifier or steam inhalation
   - Over-the-counter medications as needed
   - Vitamin C and zinc supplements
   - Honey for cough (not for children <1 year)

3. **Prevention:**
   - Regular handwashing
   - Avoid touching face
   - Stay away from sick individuals
   - Annual flu vaccination
   - Adequate sleep and nutrition

4. **Seek Medical Help if:**
   - Symptoms lasting >10 days
   - High fever >103°F (39.4°C)
   - Difficulty breathing or chest pain
   - Severe or worsening symptoms
   - Confusion or severe weakness
        """
    },
    "general_wellness": {
        "keywords": ["wellness", "healthy", "prevention", "lifestyle", "fitness"],
        "protocol": """
**General Wellness Guidelines:**

1. **Nutrition:**
   - Balanced diet with fruits, vegetables, whole grains
   - Adequate protein intake
   - Limit processed foods, sugar, and saturated fats
   - Stay hydrated (8-10 glasses water daily)

2. **Physical Activity:**
   - 150 minutes moderate exercise weekly
   - Include strength training 2x/week
   - Regular stretching and flexibility work
   - Reduce sedentary time

3. **Sleep:**
   - 7-9 hours for adults
   - Consistent sleep schedule
   - Good sleep hygiene (dark, cool room)

4. **Mental Health:**
   - Stress management techniques
   - Regular social connections
   - Mindfulness or meditation
   - Seek help when needed

5. **Preventive Care:**
   - Regular check-ups and screenings
   - Stay up-to-date on vaccinations
   - Dental and eye exams
   - Know your family health history
        """
    }
}

REFUND_POLICY = """
**Disha Health Coach - Refund Policy:**

1. **Subscription Cancellation:**
   - Cancel anytime from your account settings
   - No questions asked within first 14 days for full refund
   - After 14 days: prorated refund for unused portion

2. **Consultation Refunds:**
   - Full refund if consultation not completed
   - Partial refund for technical issues (case-by-case)
   - No refund after consultation completion

3. **Processing Time:**
   - Refunds processed within 5-7 business days
   - Original payment method used for refund

4. **How to Request:**
   - Email: support@disha.health
   - Include: Account email, reason, order number
   - Response within 24-48 hours

5. **Special Cases:**
   - Medical emergencies: Contact support immediately
   - Service dissatisfaction: We'll work to resolve first
   - Technical issues: Support will troubleshoot before refund
"""

GENERAL_POLICIES = """
**Disha Health Coach - General Policies:**

1. **Privacy & Data:**
   - Your health data is encrypted and secure
   - HIPAA compliant storage
   - Never shared without explicit consent
   - You can request data deletion anytime

2. **Service Limitations:**
   - AI health coach is for informational purposes
   - Not a replacement for professional medical advice
   - Always consult healthcare provider for serious concerns
   - Emergency situations: Call emergency services immediately

3. **Response Times:**
   - AI responses: Immediate
   - Human support: Within 24 hours
   - Urgent medical queries: Redirected to appropriate care

4. **Service Availability:**
   - 24/7 AI health coach access
   - Scheduled maintenance windows announced in advance
   - Mobile app and web platform supported
"""


def find_relevant_protocol(message: str) -> str:
    """Find relevant medical protocol based on message content"""
    message_lower = message.lower()
    relevant_protocols = []

    # Check for refund/policy keywords
    if any(keyword in message_lower for keyword in ["refund", "cancel", "money back", "subscription"]):
        relevant_protocols.append(REFUND_POLICY)

    if any(keyword in message_lower for keyword in ["policy", "privacy", "data", "security"]):
        relevant_protocols.append(GENERAL_POLICIES)

    # Check medical protocols
    for condition, protocol_data in MEDICAL_PROTOCOLS.items():
        if any(keyword in message_lower for keyword in protocol_data["keywords"]):
            relevant_protocols.append(protocol_data["protocol"])

    if relevant_protocols:
        return "\n\n---\n\n".join(relevant_protocols)

    return ""
