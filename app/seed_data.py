#!/usr/bin/env python3
"""
Data seeding script for Customer Support Bot
Populates the database with sample FAQ data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, FAQ, create_tables
from datetime import datetime

def seed_faq_data():
    """Seed the database with sample FAQ data"""
    
    # Create tables if they don't exist
    create_tables()
    
    # Sample FAQ data
    faqs = [
        {
            "question": "What payment methods do you accept?",
            "answer": "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, Apple Pay, Google Pay, and bank transfers. All payments are processed securely through our encrypted payment gateway.",
            "category": "Payment"
        },
        {
            "question": "How long does shipping take?",
            "answer": "Standard shipping takes 3-5 business days. Express shipping (1-2 business days) and overnight shipping are also available for an additional fee. International shipping typically takes 7-14 business days depending on the destination.",
            "category": "Shipping"
        },
        {
            "question": "What is your return policy?",
            "answer": "We offer a 30-day return policy for most items. Items must be in original condition with all tags attached. Returns are free for defective items. For other returns, customers are responsible for return shipping costs.",
            "category": "Returns"
        },
        {
            "question": "Do you ship internationally?",
            "answer": "Yes, we ship to over 50 countries worldwide. International shipping rates and delivery times vary by location. Some restrictions may apply to certain products due to local regulations.",
            "category": "Shipping"
        },
        {
            "question": "How can I track my order?",
            "answer": "Once your order ships, you'll receive a tracking number via email. You can also track your order by logging into your account and visiting the 'Order History' section. Real-time tracking updates are available on our website.",
            "category": "Orders"
        },
        {
            "question": "What if my item arrives damaged?",
            "answer": "If your item arrives damaged, please take photos and contact our customer service within 48 hours of delivery. We'll arrange for a replacement or refund and cover the return shipping costs.",
            "category": "Returns"
        },
        {
            "question": "Do you offer discounts for bulk orders?",
            "answer": "Yes, we offer volume discounts for orders of 10+ items. Please contact our sales team for a custom quote. Business customers may also qualify for additional discounts and special pricing.",
            "category": "Pricing"
        },
        {
            "question": "Can I cancel my order after it's placed?",
            "answer": "Orders can be cancelled within 2 hours of placement if they haven't been processed for shipping. After that, you may need to wait for delivery and use our return process. Contact customer service immediately if you need to cancel.",
            "category": "Orders"
        },
        {
            "question": "What warranty do you provide?",
            "answer": "Most products come with a 1-year manufacturer warranty. Extended warranties are available for purchase on select items. Warranty coverage varies by product category and manufacturer.",
            "category": "Warranty"
        },
        {
            "question": "How do I contact customer service?",
            "answer": "You can reach our customer service team via live chat (available 24/7), email at support@example.com, or phone at 1-800-EXAMPLE. Our phone support is available Monday-Friday 9 AM-6 PM EST.",
            "category": "Support"
        },
        {
            "question": "Do you have a loyalty program?",
            "answer": "Yes! Our rewards program gives you points for every purchase. Points can be redeemed for discounts on future orders. You'll also receive exclusive offers and early access to sales events.",
            "category": "Loyalty"
        },
        {
            "question": "What sizes do your clothing items come in?",
            "answer": "Our clothing is available in sizes XS through 3XL. We also offer petite and plus-size options for select items. Detailed size charts are available on each product page to help you find the perfect fit.",
            "category": "Products"
        },
        {
            "question": "Can I save items to a wishlist?",
            "answer": "Yes! You can create multiple wishlists and save items for later. Wishlists can be shared with friends and family, and you'll be notified when items go on sale or come back in stock.",
            "category": "Account"
        },
        {
            "question": "What if I receive the wrong item?",
            "answer": "If you receive the wrong item, please contact us immediately. We'll arrange for the correct item to be shipped and cover the return shipping for the incorrect item. We apologize for any inconvenience.",
            "category": "Returns"
        },
        {
            "question": "Do you offer gift wrapping?",
            "answer": "Yes, gift wrapping is available for $5.99 per item. You can add this option during checkout. We also offer personalized gift messages that will be included with your order.",
            "category": "Services"
        }
    ]
    
    db = SessionLocal()
    try:
        # Check if FAQs already exist
        existing_count = db.query(FAQ).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} FAQ items. Skipping seeding.")
            return
        
        # Insert FAQ data
        for faq_data in faqs:
            faq = FAQ(
                question=faq_data["question"],
                answer=faq_data["answer"],
                category=faq_data["category"],
                created_at=datetime.utcnow()
            )
            db.add(faq)
        
        db.commit()
        print(f"Successfully seeded {len(faqs)} FAQ items into the database.")
        
    except Exception as e:
        print(f"Error seeding FAQ data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding FAQ data...")
    seed_faq_data()
    print("Data seeding completed!")
