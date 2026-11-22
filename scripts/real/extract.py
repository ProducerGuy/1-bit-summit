"""Pull the PyTorch weight archive out of the spaCy package without executing anything from it.
The tensors are read with a restricted unpickler that only builds numpy arrays."""
import sys, zipfile, io, pickle, numpy as np
whl, out = sys.argv[1], sys.argv[2]
blob = zipfile.ZipFile(whl).read('en_core_web_trf/en_core_web_trf-3.7.3/transformer/model')
i = blob.find(b'PK\x03\x04'); j = blob.rfind(b'PK\x05\x06')
print('zip start', i, 'eocd', j, 'len', len(blob))
z = zipfile.ZipFile(io.BytesIO(blob[i:j + 22]))
names = z.namelist(); pkl = [n for n in names if n.endswith('data.pkl')][0]; root = pkl[:-len('data.pkl')]
print(len(names), 'entries; pickle', pkl)
class Stor:
    def __init__(s, dtype): s.dtype = dtype
DT = {'FloatStorage': np.float32, 'HalfStorage': np.float16, 'LongStorage': np.int64, 'DoubleStorage': np.float64,
      'IntStorage': np.int32, 'BoolStorage': np.bool_, 'ByteStorage': np.uint8}
def rebuild(storage, offset, size, stride, *a):
    arr = storage[offset:offset + int(np.prod(size)) if size else offset + 1]
    return arr.reshape(size)
class U(pickle.Unpickler):
    def find_class(s, mod, name):
        if mod == 'torch._utils' and name == '_rebuild_tensor_v2': return rebuild
        if mod == 'torch._utils' and name == '_rebuild_parameter': return lambda data, rg, bh: data
        if mod == 'torch' and name in DT: return Stor(DT[name])
        if mod == 'collections' and name == 'OrderedDict':
            import collections; return collections.OrderedDict
        raise pickle.UnpicklingError(f'blocked {mod}.{name}')
    def persistent_load(s, pid):
        _, st, key, loc, n = pid
        return np.frombuffer(z.read(root + 'data/' + key), dtype=st.dtype)
sd = U(io.BytesIO(z.read(pkl))).load()
keep = {k: np.array(v) for k, v in sd.items() if getattr(v, 'ndim', 0) >= 1}
print(len(keep), 'tensors;', sum(v.size for v in keep.values()) / 1e6, 'M parameters')
for k in list(keep)[:14]: print(' ', k, keep[k].shape)
np.savez(out, **keep)
