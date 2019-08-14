## Visor Test
- Automate user
- Take screen captures (temporary until can get from frame buffer)
- Process indexes to localize user
- Given a test image, should produce other frames that are similar

## To Do
- Check world type
- Better indexing algorithm (Current: average of each R,G and B values)
- Want: < 3% False Negative, minimum False Positive

Progress:
- Avg RGB : 33.6% FN; 34.0% FP
- RGB Frequency : >40% FN; >40% FP
- Avg RGB with 100 divisions : 7.2% FN; 33.4% FP
- Avg RGB with 100 divisions and continuity score : 2.73% FN; 23.7% FP