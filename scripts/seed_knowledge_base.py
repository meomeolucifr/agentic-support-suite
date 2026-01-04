"""Seed knowledge base with comprehensive sample cases."""
import asyncio
import sys
import os
import uuid
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.vector_db.chroma_client import add_case
from tools.database.postgres import get_db_session
from tools.database.models.similar_case import SimilarCase


# Comprehensive sample cases covering all categories and scenarios
SAMPLE_CASES = [
    # BILLING Category
    {
        "category": "BILLING",
        "subcategory": "DUPLICATE_CHARGE",
        "issue": "I was charged twice for my order #12345. I see two identical charges of $89.99 on my credit card statement dated yesterday. This is unacceptable and I want an immediate refund.",
        "resolution": "Duplicate charges occur when payment processing encounters network issues or customer clicks submit multiple times. Resolution steps: 1) Verify both charges in payment system (confirmed: two identical $89.99 charges), 2) Process immediate refund for duplicate charge via payment gateway, 3) Add $10 goodwill credit to customer account, 4) Send email confirmation with refund reference number, 5) Follow up in 3-5 business days to confirm refund posted. Result: Customer satisfied, refund processed within 2 hours, goodwill credit applied.",
        "satisfaction": 9
    },
    {
        "category": "BILLING",
        "subcategory": "REFUND_REQUEST",
        "issue": "I want a refund for order #67890. I ordered the wrong size and returned it last week, but haven't received my money back yet. It's been 10 days.",
        "resolution": "Refund processing workflow: 1) Check return status in system (confirmed: item received and inspected), 2) Verify refund eligibility (within 30-day return window - yes), 3) Process refund to original payment method (credit card ending in 1234), 4) Refund will appear in 5-7 business days, 5) Send confirmation email with refund amount ($129.99) and expected posting date. For future reference, refunds typically process within 5-7 business days after we receive and inspect the return.",
        "satisfaction": 8
    },
    {
        "category": "BILLING",
        "subcategory": "UNEXPECTED_CHARGE",
        "issue": "I see a charge of $29.99 on my card from your company but I don't recognize it. What is this for? I didn't make any purchase recently.",
        "resolution": "Unexpected charge investigation: 1) Check charge description and date (found: recurring subscription charge for Premium Plan), 2) Review customer account (confirmed: customer subscribed to Premium Plan 3 months ago with auto-renewal), 3) Check if customer was notified (yes, email sent 7 days before renewal), 4) Explain charge to customer and offer options: cancel subscription with prorated refund, or continue with reminder setup. Customer chose to cancel - processed cancellation and prorated refund of $15.00.",
        "satisfaction": 7
    },
    {
        "category": "BILLING",
        "subcategory": "PAYMENT_FAILED",
        "issue": "My payment keeps failing when I try to checkout. I've tried two different credit cards and both say declined. My cards work fine elsewhere.",
        "resolution": "Payment failure troubleshooting: 1) Check payment gateway logs (no errors found), 2) Verify card details match billing address exactly, 3) Check for AVS (Address Verification System) mismatches, 4) Common causes: billing address typo, card security code incorrect, card expired, insufficient funds, bank fraud protection blocking transaction. Solution: Customer updated billing address to match card statement exactly, re-entered CVV code, payment processed successfully. If still fails, contact bank to approve transaction.",
        "satisfaction": 8
    },
    
    # ACCOUNT Category
    {
        "category": "ACCOUNT",
        "subcategory": "PASSWORD_RESET",
        "issue": "I forgot my password and can't log in. I tried the 'Forgot Password' link but never received the email. I've checked spam folder too.",
        "resolution": "Password reset process: 1) Verify email address in system (confirmed: email@example.com is registered), 2) Check email delivery logs (email sent successfully 5 minutes ago), 3) Resend password reset email with new link (valid for 1 hour), 4) If still not received, check email filters and spam settings, 5) Alternative: security questions or phone verification. Customer received second email and successfully reset password. Tip: Reset links expire after 1 hour for security.",
        "satisfaction": 8
    },
    {
        "category": "ACCOUNT",
        "subcategory": "EMAIL_CHANGE",
        "issue": "I need to change my email address because I'm switching jobs. My current email is old-email@company.com and I want to use new-email@personal.com",
        "resolution": "Email change process: 1) Verify current account ownership (security questions answered correctly), 2) Initiate email change request, 3) Send verification email to new address (new-email@personal.com), 4) Customer clicks verification link in new email, 5) Send confirmation to old email address, 6) Update account email address. Important: Old email receives notification of change. If customer doesn't have access to old email, requires additional identity verification. Process completed successfully.",
        "satisfaction": 9
    },
    {
        "category": "ACCOUNT",
        "subcategory": "ACCOUNT_LOCKED",
        "issue": "My account is locked. It says 'Account temporarily locked due to multiple failed login attempts'. I didn't try logging in multiple times though.",
        "resolution": "Account lock investigation: 1) Check login attempt logs (found: 5 failed attempts from IP address 192.168.1.100 in last 10 minutes), 2) Verify if customer recognizes IP address (customer confirms it's their home IP), 3) Possible causes: password typo, Caps Lock on, browser autofill issue, or security breach. Solution: Unlock account after identity verification, reset password as precaution, enable two-factor authentication for added security. Account unlocked, password reset link sent. Customer advised to use strong password and enable 2FA.",
        "satisfaction": 7
    },
    {
        "category": "ACCOUNT",
        "subcategory": "PROFILE_UPDATE",
        "issue": "I want to update my profile information - change my name and phone number. How do I do that?",
        "resolution": "Profile update steps: 1) Log into account, 2) Navigate to Account Settings > Profile, 3) Click 'Edit' next to name or phone number, 4) Enter new information, 5) For phone number changes, verify new number via SMS code, 6) Save changes. Note: Name changes may require identity verification for security. Phone number changes require SMS verification. Profile updated successfully. Customer can now see updated information in account dashboard.",
        "satisfaction": 9
    },
    
    # SHIPPING Category
    {
        "category": "SHIPPING",
        "subcategory": "TRACKING",
        "issue": "Where is my order? I placed it 5 days ago and haven't received a tracking number. Order #98765.",
        "resolution": "Order tracking assistance: 1) Look up order #98765 in system (found: order placed 5 days ago, status: 'Shipped'), 2) Retrieve tracking number from shipping provider (tracking: 1Z999AA10123456784), 3) Check tracking status (current: 'In Transit - Expected delivery tomorrow'), 4) Provide customer with tracking number and carrier website link, 5) Set up email notifications for delivery updates. Order is on track, expected delivery tomorrow. Customer can track at carrier website using provided tracking number.",
        "satisfaction": 8
    },
    {
        "category": "SHIPPING",
        "subcategory": "DELAYED_DELIVERY",
        "issue": "My order is late. It was supposed to arrive 3 days ago according to the tracking. The last update says 'In Transit' but no movement for 4 days.",
        "resolution": "Delayed delivery investigation: 1) Check tracking details (confirmed: package stuck at distribution center for 4 days), 2) Contact carrier (carrier reports: weather delay and high volume), 3) Check if package is lost (carrier confirms: package located, will resume transit), 4) Options: Wait for delivery (expected in 2-3 days), or request replacement/refund. Customer chose to wait. Offered $10 credit for inconvenience. Package delivered 2 days later. Customer satisfied with resolution.",
        "satisfaction": 7
    },
    {
        "category": "SHIPPING",
        "subcategory": "WRONG_ADDRESS",
        "issue": "I entered the wrong shipping address when ordering. I need to change it before it ships. Order #11111.",
        "resolution": "Address change process: 1) Check order status (found: order still processing, not yet shipped), 2) Update shipping address in order system, 3) Verify new address format (confirmed: valid address), 4) Send confirmation email with updated address, 5) If order already shipped, contact carrier for address correction (may incur fee). Successfully updated address. Order will ship to new address. Customer advised to double-check address before future orders.",
        "satisfaction": 9
    },
    {
        "category": "SHIPPING",
        "subcategory": "DAMAGED_PACKAGE",
        "issue": "My package arrived damaged. The box was crushed and the item inside is broken. I need a replacement or refund.",
        "resolution": "Damaged package resolution: 1) Request photos of damaged package and item (customer provided photos), 2) Verify damage (confirmed: significant damage, item unusable), 3) Options: Full refund or replacement with expedited shipping. Customer chose replacement. 4) Process replacement order with expedited shipping (free), 5) Provide return label for damaged item (optional, customer can discard), 6) Send confirmation email. Replacement shipped next day with expedited delivery. Customer very satisfied with quick resolution.",
        "satisfaction": 9
    },
    {
        "category": "SHIPPING",
        "subcategory": "MISSING_ITEM",
        "issue": "I received my order but one item is missing. I ordered 3 items but only received 2. Order #22222.",
        "resolution": "Missing item investigation: 1) Check order details (confirmed: order should contain 3 items), 2) Review shipping manifest (found: only 2 items packed), 3) Check if item shipped separately (no separate shipment found), 4) Verify item availability (item in stock), 5) Options: Ship missing item immediately with expedited shipping, or full refund for missing item. Customer chose immediate shipment. Missing item shipped same day with expedited delivery. Customer received item next day. Apology email sent with $5 credit.",
        "satisfaction": 8
    },
    
    # TECHNICAL Category
    {
        "category": "TECHNICAL",
        "subcategory": "LOGIN_ISSUE",
        "issue": "I can't log into my account. It says my password is incorrect but I'm 100% sure it's right. I've tried multiple times.",
        "resolution": "Login troubleshooting: 1) Check account status (account active, not locked), 2) Verify password requirements (customer password meets requirements), 3) Common causes: Caps Lock enabled, browser autofill using old password, special characters not typed correctly, account compromised. Solution: Reset password via email link, clear browser cache and cookies, try incognito mode, check keyboard language settings. Customer reset password and successfully logged in. Advised to save password in secure password manager.",
        "satisfaction": 7
    },
    {
        "category": "TECHNICAL",
        "subcategory": "FEATURE_NOT_WORKING",
        "issue": "The search feature on your website isn't working. When I search for products, nothing shows up even though I know items exist.",
        "resolution": "Feature troubleshooting: 1) Test search functionality (confirmed: working on our end), 2) Check customer's browser and device (Chrome on Windows 11), 3) Common causes: Browser cache issue, JavaScript disabled, ad blocker interfering, browser extension conflict. Solution: Clear browser cache and cookies, disable browser extensions one by one, try different browser, check if JavaScript is enabled. Customer cleared cache and search worked. Issue resolved. Advised to keep browser updated.",
        "satisfaction": 8
    },
    {
        "category": "TECHNICAL",
        "subcategory": "MOBILE_APP_ISSUE",
        "issue": "Your mobile app keeps crashing when I try to view my orders. I'm using iPhone 12 with iOS 16. This started happening after the last update.",
        "resolution": "Mobile app crash investigation: 1) Check app version (customer using v2.1.0, latest is v2.1.2), 2) Review crash reports (found: known bug in v2.1.0 affecting iOS 16), 3) Solution: Update app to latest version (v2.1.2 fixes the crash), 4) If update doesn't help: Delete and reinstall app, restart device, check iOS updates. Customer updated app and issue resolved. Bug fix in v2.1.2 addressed the crash. Customer satisfied.",
        "satisfaction": 8
    },
    {
        "category": "TECHNICAL",
        "subcategory": "PAYMENT_GATEWAY_ERROR",
        "issue": "I'm getting an error when trying to checkout. It says 'Payment gateway error' and won't let me complete my purchase.",
        "resolution": "Payment gateway error troubleshooting: 1) Check payment gateway status (operational, no outages), 2) Review error logs (found: timeout error on customer's connection), 3) Common causes: Slow internet connection, browser timeout, payment gateway temporary issue, card issuer problem. Solution: Retry payment (sometimes resolves temporary issues), check internet connection, try different payment method, clear browser cache, try different browser or device. Customer retried with stable connection and payment processed successfully.",
        "satisfaction": 7
    },
    
    # PRODUCT Category
    {
        "category": "PRODUCT",
        "subcategory": "WRONG_ITEM",
        "issue": "I received the wrong item. I ordered a blue shirt size Large but received a red shirt size Medium. Order #33333.",
        "resolution": "Wrong item resolution: 1) Verify order details (confirmed: customer ordered blue shirt size L), 2) Check what was shipped (confirmed: red shirt size M shipped by mistake), 3) Options: Return for correct item with free return shipping, or keep wrong item with partial refund. Customer chose return and replacement. 4) Process return label (free), 5) Ship correct item immediately with expedited shipping, 6) Send confirmation email. Correct item shipped same day. Customer received correct item in 2 days. Apology and $10 credit provided.",
        "satisfaction": 8
    },
    {
        "category": "PRODUCT",
        "subcategory": "PRODUCT_DEFECT",
        "issue": "The product I received is defective. The power button doesn't work and the screen flickers. I just opened it today.",
        "resolution": "Defective product resolution: 1) Request photos/video of defect (customer provided video showing issue), 2) Verify defect (confirmed: manufacturing defect), 3) Check warranty status (within 30-day return window), 4) Options: Full refund or replacement. Customer chose replacement. 5) Process replacement with expedited shipping (free), 6) Provide return label for defective item, 7) Send confirmation email. Replacement shipped next day. Customer received working product. Quality team notified of defect pattern.",
        "satisfaction": 9
    },
    {
        "category": "PRODUCT",
        "subcategory": "SIZE_ISSUE",
        "issue": "The item doesn't fit. I ordered size Medium based on the size chart, but it's too small. Can I exchange it for a Large?",
        "resolution": "Size exchange process: 1) Verify return eligibility (within 30-day return window - yes), 2) Check size availability (Large in stock), 3) Process exchange: Return Medium, ship Large with free return shipping, 4) If size out of stock: Full refund option, 5) Send return label and confirmation email. Exchange processed. Customer returned Medium, received Large. Size chart updated based on feedback. Customer satisfied.",
        "satisfaction": 8
    },
    
    # GENERAL Category
    {
        "category": "GENERAL",
        "subcategory": "QUESTION",
        "issue": "Do you ship internationally? I'm in Canada and want to know shipping costs and delivery times.",
        "resolution": "International shipping information: 1) Check shipping options (yes, we ship to Canada), 2) Shipping methods: Standard (7-14 business days, $15), Express (3-5 business days, $35), 3) Customs and duties: Customer responsible for import fees, 4) Tracking: Full tracking provided, 5) Return policy: International returns accepted within 30 days, customer pays return shipping. Customer placed order with Express shipping. Order delivered in 4 days. Customer satisfied with service.",
        "satisfaction": 9
    },
    {
        "category": "GENERAL",
        "subcategory": "COMPLAINT",
        "issue": "I'm very disappointed with your service. My last 3 orders have all had issues - late delivery, wrong items, and poor packaging. This is unacceptable.",
        "resolution": "Complaint resolution: 1) Review customer order history (confirmed: 3 recent orders with issues), 2) Apologize sincerely for poor experience, 3) Investigate root causes (identified: warehouse processing errors), 4) Immediate actions: $50 account credit, expedited processing for future orders, dedicated support contact, 5) Long-term: Escalate to operations team for process improvement. Customer accepted credit and appreciated personal attention. Future orders processed smoothly. Customer retention achieved.",
        "satisfaction": 7
    },
    {
        "category": "GENERAL",
        "subcategory": "FEEDBACK",
        "issue": "I love your products but wish you had more color options. Will you be adding more colors soon?",
        "resolution": "Feedback acknowledgment: 1) Thank customer for feedback, 2) Check product roadmap (new colors planned for next season), 3) Add customer to notification list for new color launches, 4) Offer early access to new colors when available, 5) Share feedback with product team. Customer added to VIP list. Received early access to new colors. Customer very satisfied and became brand advocate.",
        "satisfaction": 10
    }
]


async def seed_knowledge_base():
    """Seed Chroma vector database with comprehensive sample cases."""
    print("=" * 60)
    print("Seeding Knowledge Base")
    print("=" * 60)
    print(f"Total cases to add: {len(SAMPLE_CASES)}")
    print()
    
    success_count = 0
    error_count = 0
    
    try:
        for i, case_data in enumerate(SAMPLE_CASES, 1):
            case_id = f"CASE_{str(uuid.uuid4())[:8].upper()}"
            
            try:
                # Combine issue and resolution for better semantic search
                combined_text = f"{case_data['issue']}\n\nResolution: {case_data['resolution']}"
                
                # Add to Chroma vector database
                await add_case(
                    case_id=case_id,
                    text=combined_text,
                    metadata={
                        "case_id": case_id,
                        "category": case_data["category"],
                        "subcategory": case_data["subcategory"],
                        "issue": case_data["issue"],
                        "resolution": case_data["resolution"],
                        "satisfaction": case_data["satisfaction"]
                    },
                    collection_name="support_cases"
                )
                
                # Also save to PostgreSQL for reference and reporting
                async for session in get_db_session():
                    db_case = SimilarCase(
                        case_id=uuid.uuid4(),
                        category=case_data["category"],
                        subcategory=case_data["subcategory"],
                        issue_description=case_data["issue"],
                        resolution=case_data["resolution"],
                        customer_satisfaction=case_data["satisfaction"],
                        vector_id=case_id
                    )
                    session.add(db_case)
                    await session.commit()
                    break
                
                success_count += 1
                print(f"[OK] ({i}/{len(SAMPLE_CASES)}) {case_data['category']} - {case_data['subcategory']}")
                
            except Exception as e:
                error_count += 1
                print(f"[ERROR] ({i}/{len(SAMPLE_CASES)}) Failed to add case: {e}")
                import traceback
                traceback.print_exc()
        
        print()
        print("=" * 60)
        print(f"Knowledge Base Seeding Complete!")
        print(f"  Success: {success_count}/{len(SAMPLE_CASES)}")
        if error_count > 0:
            print(f"  Errors: {error_count}/{len(SAMPLE_CASES)}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] Fatal error seeding knowledge base: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(seed_knowledge_base())
