// ```÷÷
const mongoose = require('mongoose');

// Example of Other Models
const FeedbackSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    content: { type: String, required: true },
    createdAt: { type: Date, default: Date.now },
});

const CoinTransactionSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    transactionType: { type: String, enum: ['purchase', 'deduction'], required: true },
    amount: { type: Number, required: true },
    createdAt: { type: Date, default: Date.now },
});

const AgencySchema = new mongoose.Schema({
    name: { type: String, required: true },
    broadcasters: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
    createdAt: { type: Date, default: Date.now },
});

module.exports = {
    Feedback: mongoose.model('Feedback', FeedbackSchema),
    CoinTransaction: mongoose.model('CoinTransaction', CoinTransactionSchema),
    Agency: mongoose.model('Agency', AgencySchema),
};
