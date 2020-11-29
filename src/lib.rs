use std::collections::HashMap;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::{pyfunction, pymodule, PyModule, PyObject, PyResult, Python};
use pyo3::{wrap_pyfunction, IntoPy};

mod intervals;

#[pyfunction]
fn fib(n: u32) -> u32 {
    if n >= 2 {
        return fib(n - 1) + fib(n - 2);
    }
    return 1;
}

/// Returns dict with keys and values swapped
#[pyfunction]
fn invert(py: Python, obj: PyObject) -> PyResult<PyObject> {
    let mut before: HashMap<String, String> = obj.extract(py)?;
    let expected_len = before.len();
    let mut after: HashMap<String, String> = HashMap::new();
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
