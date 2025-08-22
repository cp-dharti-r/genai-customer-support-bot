// Global variables
let currentProvider = null;
let currentSessionId = null;
let currentConversationId = null;
let selectedRating = 0;

// DOM elements
const providerButtons = document.getElementById('providerButtons');
const currentProviderSpan = document.getElementById('currentProvider');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const ratingModal = document.getElementById('ratingModal');
const closeModal = document.querySelector('.close');
const ratingStars = document.querySelectorAll('.rating-stars i');
const feedbackInput = document.getElementById('feedbackInput');
const submitRating = document.getElementById('submitRating');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadAnalytics();
    loadConversationHistory();
});

// Initialize the application
async function initializeApp() {
    try {
        // Load available providers
        const providers = await fetchProviders();
        renderProviderButtons(providers);
        
        // Generate session ID
        currentSessionId = generateSessionId();
        
        console.log('Application initialized successfully');
    } catch (error) {
        console.error('Failed to initialize application:', error);
        showMessage('Failed to initialize application. Please refresh the page.', 'error');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Send message
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Rating modal
    closeModal.addEventListener('click', closeRatingModal);
    window.addEventListener('click', function(e) {
        if (e.target === ratingModal) {
            closeRatingModal();
        }
    });
    
    // Rating stars
    ratingStars.forEach(star => {
        star.addEventListener('click', function() {
            selectRating(parseInt(this.dataset.rating));
        });
    });
    
    // Submit rating
    submitRating.addEventListener('click', submitRatingHandler);
    
    // Tab switching
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });
}

// Fetch available providers from API
async function fetchProviders() {
    try {
        const response = await fetch('/api/providers');
        if (!response.ok) {
            throw new Error('Failed to fetch providers');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching providers:', error);
        return [];
    }
}

// Render provider selection buttons
function renderProviderButtons(providers) {
    providerButtons.innerHTML = '';
    
    providers.forEach(provider => {
        const button = document.createElement('button');
        button.className = 'provider-btn';
        button.textContent = provider.name.charAt(0).toUpperCase() + provider.name.slice(1);
        button.dataset.provider = provider.name;
        
        if (!provider.available) {
            button.classList.add('unavailable');
            button.title = 'API key not configured';
        } else {
            button.addEventListener('click', () => selectProvider(provider.name));
        }
        
        providerButtons.appendChild(button);
    });
}

// Select a provider
function selectProvider(providerName) {
    // Update active state
    document.querySelectorAll('.provider-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-provider="${providerName}"]`).classList.add('active');
    
    // Update current provider
    currentProvider = providerName;
    currentProviderSpan.textContent = providerName.charAt(0).toUpperCase() + providerName.slice(1);
    
    // Enable chat input
    messageInput.disabled = false;
    sendButton.disabled = false;
    
    // Add welcome message
    addBotMessage(`Hello! I'm your ${providerName} powered customer support assistant. How can I help you today?`);
    
    console.log(`Provider selected: ${providerName}`);
}

// Send a message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || !currentProvider) return;
    
    // Add user message to chat
    addUserMessage(message);
    messageInput.value = '';
    
    // Show loading state
    const loadingMessage = addBotMessage('<div class="spinner"></div> Processing...', true);
    
    try {
        // Send message to API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                provider: currentProvider,
                session_id: currentSessionId
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to send message');
        }
        
        const result = await response.json();
        
        // Remove loading message and add bot response
        loadingMessage.remove();
        addBotMessage(result.response);
        
        // Store conversation ID for rating
        currentConversationId = result.conversation_id;
        
        // Add rating button
        addRatingButton();
        
        // Refresh analytics and history
        loadAnalytics();
        loadConversationHistory();
        
    } catch (error) {
        console.error('Error sending message:', error);
        loadingMessage.remove();
        addBotMessage('Sorry, I encountered an error. Please try again.');
    }
}

// Add user message to chat
function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <i class="fas fa-user"></i>
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add bot message to chat
function addBotMessage(message, isTemporary = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <i class="fas fa-robot"></i>
            <p>${message}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    return messageDiv;
}

// Add rating button to the last bot message
function addRatingButton() {
    const lastBotMessage = chatMessages.querySelector('.bot-message:last-child');
    if (lastBotMessage) {
        const ratingButton = document.createElement('button');
        ratingButton.className = 'rate-button';
        ratingButton.textContent = 'Rate Response';
        ratingButton.addEventListener('click', () => openRatingModal());
        
        const buttonContainer = document.createElement('div');
        buttonContainer.style.textAlign = 'right';
        buttonContainer.style.marginTop = '10px';
        buttonContainer.appendChild(ratingButton);
        
        lastBotMessage.appendChild(buttonContainer);
    }
}

// Open rating modal
function openRatingModal() {
    ratingModal.style.display = 'block';
    selectedRating = 0;
    feedbackInput.value = '';
    updateRatingStars();
}

// Close rating modal
function closeRatingModal() {
    ratingModal.style.display = 'none';
}

// Select rating
function selectRating(rating) {
    selectedRating = rating;
    updateRatingStars();
}

// Update rating stars display
function updateRatingStars() {
    ratingStars.forEach((star, index) => {
        if (index < selectedRating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

// Submit rating
async function submitRatingHandler() {
    if (!selectedRating || !currentConversationId) return;
    
    try {
        const response = await fetch('/api/rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                conversation_id: currentConversationId,
                rating: selectedRating,
                feedback: feedbackInput.value.trim()
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to submit rating');
        }
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('Rating submitted successfully!', 'success');
            closeRatingModal();
            
            // Refresh analytics
            loadAnalytics();
            loadConversationHistory();
        } else {
            showMessage('Failed to submit rating. Please try again.', 'error');
        }
        
    } catch (error) {
        console.error('Error submitting rating:', error);
        showMessage('Failed to submit rating. Please try again.', 'error');
    }
}

// Load analytics data
async function loadAnalytics() {
    try {
        const response = await fetch('/api/analytics');
        if (!response.ok) {
            throw new Error('Failed to fetch analytics');
        }
        
        const analytics = await response.json();
        renderAnalytics(analytics);
        
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

// Render analytics data
function renderAnalytics(analytics) {
    // Daily stats
    renderDailyStats(analytics.daily_stats);
    
    // Weekly stats
    renderWeeklyStats(analytics.weekly_stats);
    
    // Provider comparison chart
    renderProviderChart(analytics.provider_comparison);
}

// Render daily stats
function renderDailyStats(stats) {
    const dailyStatsContainer = document.getElementById('dailyStats');
    dailyStatsContainer.innerHTML = `
        <div class="stat-card">
            <div class="stat-value">${stats.total_conversations}</div>
            <div class="stat-label">Today's Conversations</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${stats.average_rating}</div>
            <div class="stat-label">Average Rating</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${stats.total_ratings}</div>
            <div class="stat-label">Total Ratings</div>
        </div>
    `;
}

// Render weekly stats
function renderWeeklyStats(stats) {
    const weeklyStatsContainer = document.getElementById('weeklyStats');
    weeklyStatsContainer.innerHTML = `
        <div class="stat-card">
            <div class="stat-value">${stats.total_conversations}</div>
            <div class="stat-label">Weekly Conversations</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${stats.average_rating}</div>
            <div class="stat-label">Average Rating</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${stats.total_ratings}</div>
            <div class="stat-label">Total Ratings</div>
        </div>
    `;
}

// Render provider comparison chart
function renderProviderChart(providerComparison) {
    const providers = Object.keys(providerComparison);
    const conversations = providers.map(p => providerComparison[p].total_conversations);
    const ratings = providers.map(p => providerComparison[p].average_rating);
    
    const trace1 = {
        x: providers,
        y: conversations,
        name: 'Total Conversations',
        type: 'bar',
        marker: { color: '#007bff' }
    };
    
    const trace2 = {
        x: providers,
        y: ratings,
        name: 'Average Rating',
        type: 'bar',
        yaxis: 'y2',
        marker: { color: '#28a745' }
    };
    
    const layout = {
        title: 'Provider Performance Comparison',
        xaxis: { title: 'LLM Provider' },
        yaxis: { title: 'Total Conversations', side: 'left' },
        yaxis2: { title: 'Average Rating', side: 'right', overlaying: 'y' },
        height: 400
    };
    
    Plotly.newPlot('providerChart', [trace1, trace2], layout);
}

// Load conversation history
async function loadConversationHistory() {
    try {
        const response = await fetch('/api/conversations');
        if (!response.ok) {
            throw new Error('Failed to fetch conversation history');
        }
        
        const conversations = await response.json();
        renderConversationHistory(conversations);
        
    } catch (error) {
        console.error('Error loading conversation history:', error);
    }
}

// Render conversation history
function renderConversationHistory(conversations) {
    const container = document.getElementById('conversationList');
    container.innerHTML = '';
    
    conversations.slice(0, 10).forEach(conversation => {
        const conversationDiv = document.createElement('div');
        conversationDiv.className = 'conversation-item';
        
        const timestamp = new Date(conversation.timestamp).toLocaleString();
        const ratingDisplay = conversation.rating ? `★ ${conversation.rating}/5` : 'Not rated';
        
        conversationDiv.innerHTML = `
            <div class="conversation-header">
                <span class="provider-badge">${conversation.llm_provider}</span>
                <span>${timestamp}</span>
            </div>
            <div class="conversation-content">
                <div class="user-question">${escapeHtml(conversation.user_message)}</div>
                <div class="bot-answer">${escapeHtml(conversation.llm_response)}</div>
            </div>
            <div class="conversation-footer">
                <span>${ratingDisplay}</span>
                ${!conversation.rating ? `<button class="rate-button" onclick="rateConversation(${conversation.id})">Rate</button>` : ''}
            </div>
        `;
        
        container.appendChild(conversationDiv);
    });
}

// Rate a conversation from history
function rateConversation(conversationId) {
    currentConversationId = conversationId;
    openRatingModal();
}

// Switch between analytics tabs
function switchTab(tabName) {
    // Update active tab button
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update active tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}Tab`).classList.add('active');
}

// Utility functions
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-${type}`;
    messageDiv.textContent = message;
    
    document.body.insertBefore(messageDiv, document.body.firstChild);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}
