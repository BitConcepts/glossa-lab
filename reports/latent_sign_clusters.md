# Latent Sign Cluster Report (Phase 5)
Generated: 2026-04-22T18:44:49Z

## CRITICAL RULES COMPLIANCE
- NO phonetic mapping performed
- NO sign collapse: every sign retains its identity
- NO token remapping: cluster labels are structural, not alphabetic
- Sequence boundaries preserved throughout

## Clustering Method
Agglomerative hierarchical clustering (Ward linkage) on 10-dimensional feature vectors:
(log_freq, start_rate, end_rate, internal_rate, positional_entropy,
 out_degree, in_degree, left_neighbor_entropy, right_neighbor_entropy, bigram_strength)

## Results Across k Values

- k=40: silhouette=0.3333, entropy_reduction=0.3204, score=0.4401
- k=60: silhouette=0.3343, entropy_reduction=0.2323, score=0.412
- k=80: silhouette=0.2959, entropy_reduction=0.1776, score=0.3485
- k=100: silhouette=0.2465, entropy_reduction=0.1327, score=0.2792

## Best k = 40 (highest composite score)

- Silhouette: 0.3333
- Entropy reduction: 0.3204
- Clusters populated: 40

## Cluster Inventory (non-empty clusters)

### Cluster 19 (12 signs)
  Members: P007, P032, P038, P041, P180, P253, P254, P258, P290, P294, P307, P393

### Cluster 1 (11 signs)
  Members: P035, P056, P142, P154, P221, P270, P283, P289, P326, P327, P349

### Cluster 3 (10 signs)
  Members: P026, P040, P048, P094, P111, P117, P151, P166, P174, P275

### Cluster 14 (9 signs)
  Members: P054, P084, P177, P182, P272, P313, P335, P352, P381

### Cluster 27 (8 signs)
  Members: P023, P076, P103, P108, P125, P126, P139, P193

### Cluster 38 (7 signs)
  Members: P003, P082, P170, P178, P251, P281, P386

### Cluster 17 (7 signs)
  Members: P031, P110, P114, P124, P127, P172, P204

### Cluster 5 (7 signs)
  Members: P075, P160, P186, P195, P285, P303, P358

### Cluster 13 (6 signs)
  Members: P010, P053, P175, P201, P309, P369

### Cluster 11 (6 signs)
  Members: P073, P092, P194, P230, P276, P316

### Cluster 6 (5 signs)
  Members: P020, P071, P293, P346, P384

### Cluster 36 (5 signs)
  Members: P043, P128, P228, P234, P382

### Cluster 4 (5 signs)
  Members: P070, P207, P232, P360, P368

### Cluster 26 (4 signs)
  Members: P000, P051, P238, P265

### Cluster 2 (4 signs)
  Members: P058, P120, P121, P325

### Cluster 8 (4 signs)
  Members: P060, P123, P147, P364

### Cluster 0 (4 signs)
  Members: P065, P089, P296, P353

### Cluster 12 (4 signs)
  Members: P280, P320, P342, P355

### Cluster 28 (3 signs)
  Members: P014, P067, P211

### Cluster 25 (3 signs)
  Members: P050, P062, P145

### Cluster 15 (3 signs)
  Members: P091, P205, P215

### Cluster 16 (3 signs)
  Members: P188, P208, P288

### Cluster 9 (3 signs)
  Members: P226, P231, P359

### Cluster 30 (2 signs)
  Members: P001, P004

### Cluster 20 (2 signs)
  Members: P009, P332

### Cluster 23 (2 signs)
  Members: P011, P144

### Cluster 7 (2 signs)
  Members: P013, P301

### Cluster 24 (2 signs)
  Members: P022, P390

### Cluster 34 (2 signs)
  Members: P095, P099

### Cluster 18 (2 signs)
  Members: P096, P136

### Cluster 10 (2 signs)
  Members: P098, P217

### Cluster 22 (2 signs)
  Members: P210, P256

### Cluster 29 (2 signs)
  Members: P268, P310

### Cluster 31 (1 signs)
  Members: P086

### Cluster 33 (1 signs)
  Members: P122

### Cluster 37 (1 signs)
  Members: P202

### Cluster 35 (1 signs)
  Members: P324

### Cluster 32 (1 signs)
  Members: P341

### Cluster 39 (1 signs)
  Members: P378

### Cluster 21 (1 signs)
  Members: P385
