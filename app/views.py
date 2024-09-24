# app/views.py
from flask import render_template, request
from . import db
from .models import BrokenLink, SpamReport
from flask import current_app as app

@app.route('/')
def dashboard():
    broken_links = BrokenLink.query.order_by(BrokenLink.checked_at.desc()).limit(10).all()
    spam_reports = SpamReport.query.order_by(SpamReport.detected_at.desc()).limit(10).all()
    return render_template('dashboard.html', broken_links=broken_links, spam_reports=spam_reports)

@app.route('/broken-links')
def view_broken_links():
    page = request.args.get('page', 1, type=int)
    broken_links = BrokenLink.query.order_by(BrokenLink.checked_at.desc()).paginate(page=page, per_page=20)
    return render_template('broken_links.html', broken_links=broken_links)

@app.route('/spam-reports')
def view_spam_reports():
    page = request.args.get('page', 1, type=int)
    spam_reports = SpamReport.query.order_by(SpamReport.detected_at.desc()).paginate(page=page, per_page=20)
    return render_template('spam_reports.html', spam_reports=spam_reports)
