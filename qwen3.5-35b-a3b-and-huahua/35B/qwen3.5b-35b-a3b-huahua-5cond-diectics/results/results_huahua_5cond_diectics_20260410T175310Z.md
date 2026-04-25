# Huahua 5-Condition Deictics Results

- Model: `Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive Q8_0`
- Routing reconstruction: `softmax_then_topk8_renorm`
- Experts: `256` total, top-`8` selected
- Layers: `40`

## Condition Means

| Cond | Label | N | Prefill RE | Prefill LT | Gen RE | Gen LT | Gen Trim RE | Gen Trim LT | KL manip | Mean gen toks |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `A` | this system | 30 | 0.956482 | 0.960332 | 0.960547 | 0.963801 | 0.960580 | 0.962316 | 0.330850 | 941.0 |
| `B` | a system | 30 | 0.955960 | 0.960353 | 0.962035 | 0.968749 | 0.961957 | 0.969312 | 0.326227 | 898.8 |
| `C` | your system | 30 | 0.956316 | 0.961933 | 0.963683 | 0.965770 | 0.963665 | 0.967817 | 0.331523 | 924.3 |
| `D` | the system | 30 | 0.956076 | 0.960353 | 0.960933 | 0.968681 | 0.961045 | 0.967448 | 0.326928 | 961.8 |
| `E` | their system | 30 | 0.956092 | 0.960705 | 0.961318 | 0.967891 | 0.961227 | 0.967658 | 0.330879 | 982.6 |

## Pairwise Tests

### `A-B`
- Prefill all-token RE: mean_diff=+0.000522, std=0.000273, gt=29/30
- Prefill last-token RE: mean_diff=-0.000020, std=0.001532, gt=15/30
- Generation all-token RE: mean_diff=-0.001488, std=0.004616, gt=14/30
- Generation last-token RE: mean_diff=-0.004948, std=0.026428, gt=13/30
- Generation trimmed RE: mean_diff=-0.001376, std=0.004708, gt=14/30
- Generation trimmed last-token RE: mean_diff=-0.006995, std=0.025800, gt=11/30
- Prefill KL-manip: mean_diff=+0.004623, std=0.005610, gt=24/30

### `A-C`
- Prefill all-token RE: mean_diff=+0.000166, std=0.000357, gt=21/30
- Prefill last-token RE: mean_diff=-0.001601, std=0.001337, gt=3/30
- Generation all-token RE: mean_diff=-0.003136, std=0.005672, gt=12/30
- Generation last-token RE: mean_diff=-0.001969, std=0.019804, gt=14/30
- Generation trimmed RE: mean_diff=-0.003085, std=0.005196, gt=11/30
- Generation trimmed last-token RE: mean_diff=-0.005501, std=0.016863, gt=10/30
- Prefill KL-manip: mean_diff=-0.000673, std=0.003121, gt=12/30

### `A-D`
- Prefill all-token RE: mean_diff=+0.000406, std=0.000296, gt=27/30
- Prefill last-token RE: mean_diff=-0.000020, std=0.001447, gt=15/30
- Generation all-token RE: mean_diff=-0.000386, std=0.004206, gt=16/30
- Generation last-token RE: mean_diff=-0.004880, std=0.023176, gt=15/30
- Generation trimmed RE: mean_diff=-0.000465, std=0.004064, gt=16/30
- Generation trimmed last-token RE: mean_diff=-0.005132, std=0.023701, gt=14/30
- Prefill KL-manip: mean_diff=+0.003922, std=0.003619, gt=26/30

### `A-E`
- Prefill all-token RE: mean_diff=+0.000391, std=0.000343, gt=25/30
- Prefill last-token RE: mean_diff=-0.000372, std=0.001499, gt=11/30
- Generation all-token RE: mean_diff=-0.000771, std=0.003765, gt=15/30
- Generation last-token RE: mean_diff=-0.004090, std=0.020758, gt=11/30
- Generation trimmed RE: mean_diff=-0.000647, std=0.003742, gt=15/30
- Generation trimmed last-token RE: mean_diff=-0.005341, std=0.019870, gt=10/30
- Prefill KL-manip: mean_diff=-0.000029, std=0.003672, gt=16/30

### `B-C`
- Prefill all-token RE: mean_diff=-0.000356, std=0.000407, gt=5/30
- Prefill last-token RE: mean_diff=-0.001581, std=0.001716, gt=5/30
- Generation all-token RE: mean_diff=-0.001648, std=0.005848, gt=11/30
- Generation last-token RE: mean_diff=+0.002979, std=0.019947, gt=20/30
- Generation trimmed RE: mean_diff=-0.001708, std=0.005510, gt=10/30
- Generation trimmed last-token RE: mean_diff=+0.001494, std=0.017785, gt=18/30
- Prefill KL-manip: mean_diff=-0.005296, std=0.004829, gt=3/30

### `B-D`
- Prefill all-token RE: mean_diff=-0.000116, std=0.000264, gt=9/30
- Prefill last-token RE: mean_diff=-0.000000, std=0.001125, gt=15/30
- Generation all-token RE: mean_diff=+0.001102, std=0.005445, gt=15/30
- Generation last-token RE: mean_diff=+0.000067, std=0.022310, gt=16/30
- Generation trimmed RE: mean_diff=+0.000911, std=0.005413, gt=15/30
- Generation trimmed last-token RE: mean_diff=+0.001863, std=0.021800, gt=18/30
- Prefill KL-manip: mean_diff=-0.000701, std=0.003503, gt=12/30

### `B-E`
- Prefill all-token RE: mean_diff=-0.000132, std=0.000283, gt=10/30
- Prefill last-token RE: mean_diff=-0.000352, std=0.001570, gt=11/30
- Generation all-token RE: mean_diff=+0.000717, std=0.004244, gt=16/30
- Generation last-token RE: mean_diff=+0.000858, std=0.017894, gt=19/30
- Generation trimmed RE: mean_diff=+0.000730, std=0.004399, gt=15/30
- Generation trimmed last-token RE: mean_diff=+0.001654, std=0.018795, gt=18/30
- Prefill KL-manip: mean_diff=-0.004652, std=0.005501, gt=6/30

### `C-D`
- Prefill all-token RE: mean_diff=+0.000240, std=0.000430, gt=23/30
- Prefill last-token RE: mean_diff=+0.001580, std=0.001700, gt=25/30
- Generation all-token RE: mean_diff=+0.002750, std=0.006378, gt=19/30
- Generation last-token RE: mean_diff=-0.002911, std=0.016167, gt=13/30
- Generation trimmed RE: mean_diff=+0.002620, std=0.005799, gt=19/30
- Generation trimmed last-token RE: mean_diff=+0.000369, std=0.015816, gt=16/30
- Prefill KL-manip: mean_diff=+0.004595, std=0.003284, gt=26/30

### `C-E`
- Prefill all-token RE: mean_diff=+0.000225, std=0.000383, gt=25/30
- Prefill last-token RE: mean_diff=+0.001229, std=0.001777, gt=24/30
- Generation all-token RE: mean_diff=+0.002365, std=0.006642, gt=18/30
- Generation last-token RE: mean_diff=-0.002121, std=0.016644, gt=13/30
- Generation trimmed RE: mean_diff=+0.002438, std=0.006017, gt=21/30
- Generation trimmed last-token RE: mean_diff=+0.000160, std=0.013784, gt=14/30
- Prefill KL-manip: mean_diff=+0.000643, std=0.003110, gt=17/30

### `D-E`
- Prefill all-token RE: mean_diff=-0.000015, std=0.000338, gt=13/30
- Prefill last-token RE: mean_diff=-0.000352, std=0.001597, gt=15/30
- Generation all-token RE: mean_diff=-0.000385, std=0.004328, gt=14/30
- Generation last-token RE: mean_diff=+0.000791, std=0.016933, gt=15/30
- Generation trimmed RE: mean_diff=-0.000182, std=0.004127, gt=15/30
- Generation trimmed last-token RE: mean_diff=-0.000209, std=0.018159, gt=16/30
- Prefill KL-manip: mean_diff=-0.003951, std=0.003935, gt=5/30

