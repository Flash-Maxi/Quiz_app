# 🧠 Flask Quiz App

A modern, interactive quiz application built with Flask that provides an engaging way to test knowledge through multiple-choice questions.

## 🌟 Features

- **Interactive Quiz Interface**: Clean, dark-themed UI with smooth user experience
- **Session-based State Management**: Tracks progress through Flask sessions
- **Randomized Questions**: Questions are shuffled for each quiz session
- **Score Tracking**: Real-time score calculation and final results display
- **Responsive Design**: Works well on desktop and mobile devices
- **JSON-based Question Storage**: Easy to modify and extend question sets

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Mystify7777/Quiz_app.git
   cd Quiz_app
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**

   ```bash
   # On Windows
   set SECRET_KEY=your-secret-key-here
   
   # On macOS/Linux
   export SECRET_KEY=your-secret-key-here
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000` to start the quiz!

## 📁 Project Structure

```bash
Quiz_app/
├── app.py                 # Main Flask application
├── questions.json         # Quiz questions database
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── static/
│   └── style.css         # CSS styling
├── templates/
│   ├── index.html        # Welcome page
│   ├── quiz.html         # Quiz interface
│   └── results.html      # Results page
└── .devcontainer/
    └── devcontainer.json # Development container config
```

## 🎮 How to Play

1. **Start**: Click "Start Quiz" on the welcome page
2. **Answer**: Select your answer from the multiple-choice options
3. **Progress**: Navigate through questions using "Next Question"
4. **Results**: View your final score and play again

## 🔧 Configuration

### Adding Questions

Edit `questions.json` to add new questions:

```json
{
  "question": "Your question here?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_answer": "Option A"
}
```

### Environment Variables

- `SECRET_KEY`: Flask session secret key (required for production)

## 🐳 Development with Dev Containers

This project includes a dev container configuration for consistent development environments.

1. **Open in Dev Container** (VS Code with Dev Containers extension)
2. **Container will auto-install** all dependencies
3. **Start developing** immediately!

## 🧪 Testing

```bash
# Run the application in debug mode
python app.py

# The app will be available at http://localhost:5000
```

## 📦 Deployment

### Using Gunicorn (Production)

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Environment Setup for Production

```bash
export SECRET_KEY="your-super-secret-production-key"
export FLASK_ENV=production
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 📋 TODO List & Roadmap

## 🔥 Phase 1: Immediate Improvements (1-2 weeks)

### Security & Configuration

- [ ] **Fix Secret Key Management**
  - [ ] Add `.env` file support with python-dotenv
  - [ ] Generate secure random secret key for production
  - [ ] Add environment-specific configurations
  - [ ] Implement proper config class structure

- [ ] **Enhanced Error Handling**
  - [ ] Add try-catch blocks around critical operations
  - [ ] Create custom error pages (404, 500)
  - [ ] Implement logging throughout the application
  - [ ] Add form validation and error messages

### User Experience

- [ ] **Answer Review System**
  - [ ] Show correct answers after quiz completion
  - [ ] Display which questions were answered correctly/incorrectly
  - [ ] Add explanations for correct answers
  - [ ] Implement question-by-question review mode

- [ ] **Progress & Visual Improvements**
  - [ ] Add visual progress bar during quiz
  - [ ] Implement loading states for form submissions
  - [ ] Add hover effects and smooth transitions
  - [ ] Improve mobile responsiveness

### Code Quality

- [ ] **Fix DevContainer Configuration**
  - [ ] Remove Streamlit references from devcontainer.json
  - [ ] Update to proper Flask development setup
  - [ ] Add proper port forwarding for Flask

## ⚡ Phase 2: Core Features (3-4 weeks)

### Database Integration

- [ ] **Migrate from JSON to Database**
  - [ ] Set up SQLAlchemy with Flask
  - [ ] Create Question, Category, User models
  - [ ] Implement database migrations
  - [ ] Add data seeding for initial questions
  - [ ] Create database backup/restore functionality

- [ ] **User Management System**
  - [ ] Implement user registration and login
  - [ ] Add password hashing with bcrypt
  - [ ] Create user profiles and preferences
  - [ ] Implement session management with Flask-Login
  - [ ] Add "Remember Me" functionality

### Question Management

- [ ] **Admin Interface**
  - [ ] Create admin dashboard for question management
  - [ ] Add CRUD operations for questions
  - [ ] Implement bulk question import/export
  - [ ] Add question validation and preview
  - [ ] Create category management system

- [ ] **Enhanced Question Types**
  - [ ] Support for True/False questions
  - [ ] Add fill-in-the-blank questions
  - [ ] Implement multiple correct answers
  - [ ] Add question difficulty levels
  - [ ] Support for image-based questions

### Testing & Quality

- [ ] **Test Suite Implementation**
  - [ ] Set up pytest for unit testing
  - [ ] Add integration tests for routes
  - [ ] Implement test coverage reporting
  - [ ] Add automated testing in CI/CD

## 🚀 Phase 3: Advanced Features (2-3 months)

### Analytics & Reporting

- [ ] **User Analytics Dashboard**
  - [ ] Track quiz attempts and scores over time
  - [ ] Generate performance reports
  - [ ] Add category-wise performance analysis
  - [ ] Implement data visualization with charts
  - [ ] Export results to CSV/PDF

- [ ] **Question Analytics**
  - [ ] Track question difficulty and success rates
  - [ ] Identify problematic questions
  - [ ] Generate question performance reports
  - [ ] A/B testing for question variations

### Advanced Quiz Features

- [ ] **Quiz Customization**
  - [ ] Allow users to select categories
  - [ ] Implement difficulty-based filtering
  - [ ] Add time limits for questions/quizzes
  - [ ] Create custom quiz lengths
  - [ ] Add practice mode vs. exam mode

- [ ] **Social Features**
  - [ ] Implement global leaderboards
  - [ ] Add friend challenges
  - [ ] Share quiz results on social media
  - [ ] Create achievement badges system
  - [ ] Add quiz completion certificates

### Performance & Scalability

- [ ] **Optimization**
  - [ ] Implement Redis for session management
  - [ ] Add database query optimization
  - [ ] Implement caching for frequently accessed data
  - [ ] Add API rate limiting
  - [ ] Optimize static asset delivery with CDN

## 🌟 Phase 4: Enterprise Features (3+ months)

### Advanced Systems

- [ ] **Real-time Features**
  - [ ] Implement WebSocket support for live quizzes
  - [ ] Add multiplayer quiz rooms
  - [ ] Real-time leaderboard updates
  - [ ] Live quiz hosting features

- [ ] **API Development**
  - [ ] Create RESTful API endpoints
  - [ ] Add API documentation with Swagger
  - [ ] Implement API authentication
  - [ ] Add rate limiting and throttling

### Mobile & Accessibility

- [ ] **Progressive Web App (PWA)**
  - [ ] Add offline support
  - [ ] Implement push notifications
  - [ ] Add install prompts
  - [ ] Cache quiz data for offline use

- [ ] **Accessibility Improvements**
  - [ ] Add ARIA labels and roles
  - [ ] Implement keyboard navigation
  - [ ] Add screen reader support
  - [ ] Include color contrast improvements
  - [ ] Add RTL language support

### DevOps & Deployment

- [ ] **Infrastructure**
  - [ ] Set up Docker containerization
  - [ ] Implement CI/CD pipeline with GitHub Actions
  - [ ] Add automated deployment to cloud platforms
  - [ ] Set up monitoring and alerting
  - [ ] Implement automated backups

## 🔧 Technical Debt & Maintenance

### Code Structure

- [ ] **Refactoring**
  - [ ] Separate routes into Blueprint modules
  - [ ] Create service layer for business logic
  - [ ] Implement repository pattern for data access
  - [ ] Add proper dependency injection

- [ ] **Code Quality Tools**
  - [ ] Set up Black for code formatting
  - [ ] Add isort for import sorting
  - [ ] Implement pylint for static analysis
  - [ ] Add mypy for type checking
  - [ ] Set up pre-commit hooks

### Documentation

- [ ] **Developer Documentation**
  - [ ] Add inline code documentation
  - [ ] Create API documentation
  - [ ] Write deployment guides
  - [ ] Add troubleshooting guides
  - [ ] Create contribution guidelines

---

## 🎯 Priority Labels

- 🔥 **Critical**: Security and stability fixes
- ⚡ **High**: Core functionality improvements
- 🚀 **Medium**: Feature enhancements
- 🌟 **Low**: Nice-to-have features

## 📊 Progress Tracking

- **Phase 1**: 0% Complete (0/20 tasks)
- **Phase 2**: 0% Complete (0/25 tasks)
- **Phase 3**: 0% Complete (0/20 tasks)
- **Phase 4**: 0% Complete (0/15 tasks)

**Overall Progress**: 0% Complete (0/80 total tasks)

---

*Last Updated: September 22, 2025*
*Next Review: October 6, 2025*
