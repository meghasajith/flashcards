from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Initialize storage
if not os.path.exists('data'):
    os.makedirs('data')

def save_flashcards():
    with open('data/flashcards.json', 'w') as f:
        json.dump(flashcard_sets, f)

def load_flashcards():
    try:
        with open('data/flashcards.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Load existing flashcards
flashcard_sets = load_flashcards()

@app.route('/')
def index():
    stats = {
        'total_sets': len(flashcard_sets),
        'total_cards': sum(len(cards) for cards in flashcard_sets.values()),
        'last_studied': session.get('last_studied', 'Never')
    }
    return render_template('index.html', flashcard_sets=flashcard_sets, stats=stats)

@app.route('/create', methods=['GET', 'POST'])
def create_flashcard_set():
    if request.method == 'POST':
        set_name = request.form['set_name'].strip()
        if not set_name:
            flash('Set name cannot be empty!', 'error')
            return redirect(url_for('create_flashcard_set'))
        
        if set_name in flashcard_sets:
            flash('A set with this name already exists!', 'error')
            return redirect(url_for('create_flashcard_set'))
        
        flashcard_sets[set_name] = []
        save_flashcards()
        flash(f'Successfully created flashcard set: {set_name}', 'success')
        return redirect(url_for('add_flashcards', set_name=set_name))
    
    return render_template('create_flashcard_set.html')

@app.route('/set/<set_name>', methods=['GET', 'POST'])
def add_flashcards(set_name):
    if set_name not in flashcard_sets:
        flash('Flashcard set not found!', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        question = request.form['question'].strip()
        answer = request.form['answer'].strip()
        
        if not question or not answer:
            flash('Both question and answer are required!', 'error')
            return redirect(url_for('add_flashcards', set_name=set_name))
        
        flashcard_sets[set_name].append({
            'question': question,
            'answer': answer,
            'created_at': datetime.now().isoformat(),
            'times_reviewed': 0,
            'times_correct': 0
        })
        save_flashcards()
        flash('Flashcard added successfully!', 'success')
        
    cards = flashcard_sets.get(set_name, [])
    return render_template('set_detail.html', set_name=set_name, cards=cards)

@app.route('/review/<set_name>')
def review_flashcards(set_name):
    if set_name not in flashcard_sets:
        flash('Flashcard set not found!', 'error')
        return redirect(url_for('index'))
    
    cards = flashcard_sets.get(set_name, [])
    if not cards:
        flash('This set has no flashcards yet!', 'warning')
        return redirect(url_for('add_flashcards', set_name=set_name))
    
    session['last_studied'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('review_flashcards.html', set_name=set_name, flashcards=cards)

@app.route('/delete/<set_name>', methods=['POST'])
def delete_flashcard_set(set_name):
    if set_name in flashcard_sets:
        del flashcard_sets[set_name]
        save_flashcards()
        flash(f'Successfully deleted flashcard set: {set_name}', 'success')
    else:
        flash('Flashcard set not found!', 'error')
    return redirect(url_for('index'))

@app.route('/api/update_progress', methods=['POST'])
def update_progress():
    data = request.get_json()
    set_name = data.get('set_name')
    card_index = data.get('card_index')
    is_correct = data.get('is_correct')
    
    if set_name in flashcard_sets and 0 <= card_index < len(flashcard_sets[set_name]):
        card = flashcard_sets[set_name][card_index]
        card['times_reviewed'] += 1
        if is_correct:
            card['times_correct'] += 1
        save_flashcards()
        return {'success': True}
    return {'success': False}, 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
