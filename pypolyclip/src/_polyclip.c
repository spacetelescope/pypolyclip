#include <stdio.h>
#include <Python.h>
#include <numpy/npy_no_deprecated_api.h>
#include <numpy/arrayobject.h>
#include "polyclip.h"



/*
NAME:
  _POLYCLIP

DESCRIPTION:
  Supplies python and numpy interfaces to the functions in the `polyclip.c`
  file.

AUTHOR:
  Russell Ryan (STScI)


*/





/* Check that an argument is an aligned, C-contiguous array of the given
   type in native byte order, and that it is writeable if it is an output.
   Return 1 if it is. Otherwise set an exception and return 0. */
static int check_array(PyArrayObject *arr,int typenum,int output,const char *name){
  if (!PyArray_EquivTypenums(PyArray_TYPE(arr),typenum)) {
    PyErr_Format(PyExc_TypeError,"%s must have dtype %s",name,
                 typenum == NPY_FLOAT32 ? "float32" : "int32");
    return 0;
  }
  if (!PyArray_IS_C_CONTIGUOUS(arr) || !PyArray_ISBEHAVED_RO(arr)) {
    PyErr_Format(PyExc_ValueError,
                 "%s must be an aligned, C-contiguous array in native byte order",
                 name);
    return 0;
  }
  if (output && PyArray_FailUnlessWriteable(arr,name) < 0) return 0;
  return 1;
}


static PyObject *py_multi(PyObject *self,PyObject *args){
  /* Function to link to the polyclip_multi function. The arrays are
     borrowed from args, which keeps them alive during the call. */
  PyArrayObject *larr,*rarr,*barr,*tarr,*pxarr,*pyarr;
  PyArrayObject *poly_indsarr,*xxarr,*yyarr,*nclip_polyarr,*areasarr;
  int n_poly;

  if (!PyArg_ParseTuple(args,"O!O!O!O!O!O!iO!O!O!O!O!",
                        &PyArray_Type,&larr,&PyArray_Type,&rarr,
                        &PyArray_Type,&barr,&PyArray_Type,&tarr,
                        &PyArray_Type,&pxarr,&PyArray_Type,&pyarr,&n_poly,
                        &PyArray_Type,&poly_indsarr,&PyArray_Type,&xxarr,
                        &PyArray_Type,&yyarr,&PyArray_Type,&nclip_polyarr,
                        &PyArray_Type,&areasarr)){
    return NULL;
  }

  if (!check_array(larr,NPY_INT32,0,"l") ||
      !check_array(rarr,NPY_INT32,0,"r") ||
      !check_array(barr,NPY_INT32,0,"b") ||
      !check_array(tarr,NPY_INT32,0,"t") ||
      !check_array(pxarr,NPY_FLOAT32,0,"px") ||
      !check_array(pyarr,NPY_FLOAT32,0,"py") ||
      !check_array(poly_indsarr,NPY_INT32,1,"poly_inds") ||
      !check_array(xxarr,NPY_INT32,1,"xx") ||
      !check_array(yyarr,NPY_INT32,1,"yy") ||
      !check_array(nclip_polyarr,NPY_INT32,1,"nclip_poly") ||
      !check_array(areasarr,NPY_FLOAT32,1,"areas")) {
    return NULL;
  }

  /* call function */
  polyclip_multi((int*)PyArray_DATA(larr),(int*)PyArray_DATA(rarr),
                 (int*)PyArray_DATA(barr),(int*)PyArray_DATA(tarr),
                 (float*)PyArray_DATA(pxarr),(float*)PyArray_DATA(pyarr),
                 n_poly,(int*)PyArray_DATA(poly_indsarr),
                 (int*)PyArray_DATA(xxarr),(int*)PyArray_DATA(yyarr),
                 (int*)PyArray_DATA(nclip_polyarr),
                 (float*)PyArray_DATA(areasarr));

  Py_RETURN_NONE;
}


static PyObject *py_single(PyObject *self,PyObject *args){
  /* Function to link to the polyclip_single function. The arrays are
     borrowed from args, which keeps them alive during the call. */
  PyArrayObject *larr,*rarr,*barr,*tarr,*pxarr,*pyarr,*nvertsarr;
  PyArrayObject *px_outarr,*py_outarr,*indsarr,*nclip_polyarr,*areasarr;
  PyArrayObject *ri_outarr;

  if (!PyArg_ParseTuple(args,"O!O!O!O!O!O!O!O!O!O!O!O!O!",
                        &PyArray_Type,&larr,&PyArray_Type,&rarr,
                        &PyArray_Type,&barr,&PyArray_Type,&tarr,
                        &PyArray_Type,&pxarr,&PyArray_Type,&pyarr,
                        &PyArray_Type,&nvertsarr,&PyArray_Type,&px_outarr,
                        &PyArray_Type,&py_outarr,&PyArray_Type,&indsarr,
                        &PyArray_Type,&nclip_polyarr,&PyArray_Type,&areasarr,
                        &PyArray_Type,&ri_outarr)){
    return NULL;
  }

  if (!check_array(larr,NPY_INT32,0,"l") ||
      !check_array(rarr,NPY_INT32,0,"r") ||
      !check_array(barr,NPY_INT32,0,"b") ||
      !check_array(tarr,NPY_INT32,0,"t") ||
      !check_array(pxarr,NPY_FLOAT32,0,"px") ||
      !check_array(pyarr,NPY_FLOAT32,0,"py") ||
      !check_array(nvertsarr,NPY_INT32,0,"nverts") ||
      !check_array(px_outarr,NPY_FLOAT32,1,"px_out") ||
      !check_array(py_outarr,NPY_FLOAT32,1,"py_out") ||
      !check_array(indsarr,NPY_INT32,1,"inds") ||
      !check_array(nclip_polyarr,NPY_INT32,1,"nclip_poly") ||
      !check_array(areasarr,NPY_FLOAT32,1,"areas") ||
      !check_array(ri_outarr,NPY_INT32,1,"ri_out")) {
    return NULL;
  }

  /* call function */
  polyclip_single(*(int*)PyArray_DATA(larr),*(int*)PyArray_DATA(rarr),
                  *(int*)PyArray_DATA(barr),*(int*)PyArray_DATA(tarr),
                  (float*)PyArray_DATA(pxarr),(float*)PyArray_DATA(pyarr),
                  *(int*)PyArray_DATA(nvertsarr),(int*)PyArray_DATA(indsarr),
                  (int*)PyArray_DATA(nclip_polyarr),
                  (float*)PyArray_DATA(areasarr),
                  (float*)PyArray_DATA(px_outarr),
                  (float*)PyArray_DATA(py_outarr),
                  (int*)PyArray_DATA(ri_outarr));

  Py_RETURN_NONE;
}




/* Collection of function names */
static PyMethodDef module_methods[]={
  { "multi", py_multi, METH_VARARGS, "A python driver to call polyclip_multi.\nA function written by J.D. Smith\n"},
  { "single", py_single, METH_VARARGS, "A python driver to call polyclip_single.\nA function written by J.D. Smith\n"},
  { NULL, NULL, 0, NULL }
};


/* Function definition to the python code */
static struct PyModuleDef _polyclip =
{
    PyModuleDef_HEAD_INIT,
    "polyclip", /* name of module */
    NULL,
    -1,
    module_methods
};


/* Function to initialize python object */
PyMODINIT_FUNC PyInit_polyclip(void)
{
  import_array();
  PyObject *module = PyModule_Create(&_polyclip);
#if defined(Py_GIL_DISABLED) && !defined(Py_LIMITED_API)
  /* Each call in polyclip.c keeps its clipping state on its own stack,
     so the module can run without the GIL on free-threaded builds. */
  if (module != NULL && PyUnstable_Module_SetGIL(module, Py_MOD_GIL_NOT_USED) < 0) {
    Py_DECREF(module);
    return NULL;
  }
#endif
  return module;
}
