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

    /* sanity check on the inputs */
    if (rel_tol < 0.0 || abs_tol < 0.0 ){
        PyErr_SetString(PyExc_ValueError,
                            "error tolerances must be non-negative");
        return NULL;
    }

    if ( a == b ){
        /* short circuit exact equality -- needed to catch two
           infinities of the same sign. And perhaps speeds things
           up a bit sometimes.
        */
        return PyBool_FromLong(1);
    }

    /* This catches the case of two infinities of opposite sign, or
       one infinity and one finite number. Two infinities of opposite
       sign would otherwise have an infinite relative tolerance.

       Two infinities of the same sign are caught by the equality check
       above.
    */

    if (Py_IS_INFINITY(a) || Py_IS_INFINITY(b)){
        return PyBool_FromLong(0);
    }

    /* now do the regular computation
       this is essentially the "weak" test from the Boost library
    */

    diff = fabs(b - a);

    result = (((diff <= fabs(rel_tol * b)) ||
                   (diff <= fabs(rel_tol * a))) ||
                   (diff <= abs_tol)) ;

    return PyBool_FromLong(result);
}

PyDoc_STRVAR(isclose_doc,
"Determine if two floating point numbers are  in value\n\n"

"Returns True if a is close in value to b. False otherwise\n\n"
":param a: one of the values to be tested\n\n"
":param b: the other value to be tested\n\n"
":param rel_tol=1e-9: The relative tolerance -- the amount of error\n"
"                     allowed, relative to the magnitude of the input\n"
"                     values.\n\n"
":param abs_tol=0.0: The minimum absolute tolerance level -- useful for\n"
"                    comparisons to zero.\n\n"
"NOTES:\n"
"-inf, inf and NaN behave similarly to the IEEE 754 Standard. That\n"
"is, NaN is not close to anything, even itself. inf and -inf are\n"
"only close to themselves.\n\n"
"See PEP-0485 for a detailed description\n");

static PyMethodDef IsCloseMethods[] = {
    {"isclose", isclose_c, METH_VARARGS | METH_KEYWORDS,
     isclose_doc},
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
