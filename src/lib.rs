use std::cmp::{Eq, PartialEq};
use std::collections::HashMap;
use std::hash::{Hash, Hasher};

use pyo3::exceptions::PyValueError;
use pyo3::prelude::{pyfunction, pymodule, PyModule, PyObject, PyResult, Python};
use pyo3::types::PyAny;
use pyo3::{wrap_pyfunction, FromPyObject, IntoPy};

mod intervals;

#[pyfunction]
fn fib(n: u32) -> u32 {
    if n >= 2 {
        return fib(n - 1) + fib(n - 2);
    }
    return 1;
}

struct HashablePyObject<'source> {
    obj: &'source PyAny,
    hash: isize,
}
impl HashablePyObject<'_> {
    fn new(obj: &PyAny, hash: isize) -> HashablePyObject {
        HashablePyObject {
            obj: obj,
            hash: hash,
        }
    }
}

impl Hash for HashablePyObject<'_> {
    fn hash<H: Hasher>(&self, state: &mut H) {
        state.write_isize(self.hash)
    }
}

impl<'source> FromPyObject<'source> for HashablePyObject<'source> {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        let hash = ob.hash()?;
        Ok(HashablePyObject::new(ob, hash))
    }
}

impl IntoPy<PyObject> for HashablePyObject<'_> {
    fn into_py(self, py: Python) -> PyObject {
        self.obj.into_py(py)
    }
}

impl PartialEq for HashablePyObject<'_> {
    fn eq(&self, other: &Self) -> bool {
        self.hash == other.hash
    }
}
impl Eq for HashablePyObject<'_> {}

/// Returns dict with keys and values swapped
#[pyfunction]
fn invert(py: Python, obj: PyObject) -> PyResult<PyObject> {
    let mut before: HashMap<HashablePyObject, HashablePyObject> = obj.extract(py)?;
    let expected_len = before.len();
    let mut after: HashMap<HashablePyObject, HashablePyObject> =
        HashMap::with_capacity(expected_len);
    for (key, value) in before.drain() {
        after.insert(value, key);
    }
    let actual_len = after.len();
    if actual_len == expected_len {
        Ok(after.into_py(py))
    } else {
        Err(PyValueError::new_err("Duplicate values in mapping"))
    }
}

#[pymodule]
fn sprigs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(fib))?;
    m.add_wrapped(wrap_pyfunction!(invert))?;

    Ok(())
}
