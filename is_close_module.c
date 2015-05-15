/* is_close implimentation in C  */

#include "Python.h"

char *is_close_doc = "This will be the docstring, when I write it";



static PyObject *
is_close_c(PyObject *self, PyObject *args, PyObject *kwargs)
{
    double a, b;
    double rel_tol = 1e-9;
    double abs_tol = 0.0;
    long result = 0;

    static char *keywords[] = {"a", "b", "rel_tol", "abs_tol", NULL};


    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd|dd:is_close",
                                     keywords,
                                     &a, &b, &rel_tol, &abs_tol
                                     ))
        return NULL;

    result = 1;

    return PyBool_FromLong(result);
}

static PyMethodDef IsCloseMethods[] = {
    {"is_close", is_close_c, METH_VARARGS | METH_KEYWORDS,
     "determine if two floating point numbers are close"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef is_close_module = {
   PyModuleDef_HEAD_INIT,
   "is_close_module",   /* name of module */
   "docstring for is_close", /* module documentation, may be NULL */
   -1,           /* size of per-interpreter state of the module,
                    or -1 if the module keeps state in global variables. */
   IsCloseMethods
};

PyMODINIT_FUNC
PyInit_is_close_module(void)
{
    return PyModule_Create(&is_close_module);
}
