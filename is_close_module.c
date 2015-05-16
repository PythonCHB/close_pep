/* is_close implimentation in C  */

#include "Python.h"

char *is_close_doc = "This will be the docstring, when I write it";



static PyObject *
isclose_c(PyObject *self, PyObject *args, PyObject *kwargs)
{
    double a, b;
    double rel_tol = 1e-9;
    double abs_tol = 0.0;
    double diff = 0.0;
    long result = 0;

    static char *keywords[] = {"a", "b", "rel_tol", "abs_tol", NULL};


    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd|dd:isclose",
                                     keywords,
                                     &a, &b, &rel_tol, &abs_tol
                                     ))
        return NULL;

    if ( a == b ){
        /* short circuit exact equality -- why not?*/
        return PyBool_FromLong(1);
    }

    diff = fabs(b - a);

    result = (((diff <= fabs(rel_tol * b)) ||
                   (diff <= fabs(rel_tol * a))) ||
                   (diff <= abs_tol)) ;

    /*(d1 <= p_fraction_tolerance && d2 <= p_fraction_tolerance)
    */
    return PyBool_FromLong(result);
}

static PyMethodDef IsCloseMethods[] = {
    {"isclose", isclose_c, METH_VARARGS | METH_KEYWORDS,
     "determine if two floating point numbers are close"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef is_close_module = {
   PyModuleDef_HEAD_INIT,
   "is_close_module",   /* name of module */
   "docstring for is_close_module module", /* module documentation, may be NULL */
   -1,           /* size of per-interpreter state of the module,
                    or -1 if the module keeps state in global variables. */
   IsCloseMethods
};

PyMODINIT_FUNC
PyInit_is_close_module(void)
{
    return PyModule_Create(&is_close_module);
}
