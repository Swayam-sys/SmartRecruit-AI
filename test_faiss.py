import numpy as np
from vector_db import save_vectors

embeddings = np.random.rand(5, 384)

save_vectors(embeddings)

print("Done")