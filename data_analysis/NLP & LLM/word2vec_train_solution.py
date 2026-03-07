import numpy as np
from collections import Counter

def train(data: str):
    """
    return: w2v_dict: dict
            - key: string (word)
            - value: np.array (embedding)
    """
    # tokenize
    words = data.split()
    if not words:
        return {}
    
    # build vocabulary
    vocab = sorted(set(words))
    word_to_idx = {w: i for i, w in enumerate(vocab)}
    vocab_size = len(vocab)
    
    # Hyperparameters
    emb_dim = 50
    window = 3
    epochs = 25
    lr = 0.03
    k_neg = 5
    
    # Initialize embeddings
    np.random.seed(42)  # for reproducibility (optional)
    W_in = np.random.uniform(-0.5, 0.5, (vocab_size, emb_dim)) / emb_dim
    W_out = np.random.uniform(-0.5, 0.5, (vocab_size, emb_dim)) / emb_dim
    
    # Compute word frequencies for negative sampling
    word_counts = Counter(words)
    counts = np.array([word_counts[w] for w in vocab], dtype=float)
    counts = counts ** 0.75
    neg_prob = counts / counts.sum()
    
    # Pre-compute context windows for all positions
    context_pairs = []
    n = len(words)
    for i in range(n):
        left = max(0, i - window)
        right = min(n, i + window + 1)
        center_word = words[i]
        c_idx = word_to_idx[center_word]
        for j in range(left, right):
            if j == i:
                continue
            context_word = words[j]
            ctx_idx = word_to_idx[context_word]
            context_pairs.append((c_idx, ctx_idx))
    
    # Convert to numpy arrays for faster processing
    context_pairs = np.array(context_pairs)
    
    for epoch in range(epochs):
        np.random.shuffle(context_pairs)
        
        for c_idx, ctx_idx in context_pairs:
            # Get vectors
            v_c = W_in[c_idx]
            v_ctx = W_out[ctx_idx]
            
            # Positive sample gradient
            dot_pos = np.dot(v_c, v_ctx)
            sig_pos = 1 / (1 + np.exp(-dot_pos))
            grad_pos = sig_pos - 1
            
            # Negative sampling - быстрая генерация
            neg_indices = np.random.choice(vocab_size, size=k_neg, p=neg_prob, replace=False)
            
            # Compute all negative gradients at once
            v_negs = W_out[neg_indices]
            dot_negs = np.dot(v_c, v_negs.T)
            sig_negs = 1 / (1 + np.exp(-dot_negs))
            grad_negs = sig_negs
            
            # Apply updates
            W_in[c_idx] -= lr * grad_pos * v_ctx
            W_out[ctx_idx] -= lr * grad_pos * v_c
            
            # Vectorized negative updates
            for neg_idx, grad_neg in zip(neg_indices, grad_negs):
                W_in[c_idx] -= lr * grad_neg * W_out[neg_idx]
                W_out[neg_idx] -= lr * grad_neg * v_c
                
    w2v_dict = {word: W_in[word_to_idx[word]] for word in vocab}
    return w2v_dict
