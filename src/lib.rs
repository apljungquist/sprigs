mod intervals;
use pyo3::prelude::{pyfunction, pymodule, PyModule, PyObject, PyResult, Python};
use pyo3::wrap_pyfunction;

#[pyfunction]
fn fib(n: u32) -> u32 {
    if n >= 2 {
        return fib(n - 1) + fib(n - 2);
    }
    return 1;
}

/// Returns dict with keys and values swapped
#[pyfunction]
fn invert(obj: PyObject) -> PyResult<PyObject> {
    Ok(obj)
}

#[pymodule]
fn sprigrs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(fib))?;
    m.add_wrapped(wrap_pyfunction!(invert))?;

    Ok(())
}
