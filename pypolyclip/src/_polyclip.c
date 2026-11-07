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





/* Release an array from PyArray_FROM_OTF. When the array is a writeback
   copy of an output argument, copy its data back to the original array if
   the call succeeded, otherwise discard it. Return 0 on success and -1 if
   the copy back failed, in which case a Python exception is set. */
static int release_array(PyObject *arr, int writeback){
  int status=0;
  if (arr == NULL) return 0;
  if (writeback) {
    status=PyArray_ResolveWritebackIfCopy((PyArrayObject*)arr);
  } else {
    PyArray_DiscardWritebackIfCopy((PyArrayObject*)arr);
  }
  Py_DECREF(arr);
  return status < 0 ? -1 : 0;
}


static PyObject *py_multi(PyObject *self,PyObject *args){
  /* Function to link to the polyclip_multi function */

  /* Create objects from the inputs */
  PyObject *lobj,*robj,*bobj,*tobj,*pxobj,*pyobj;
  PyObject *n_polyobj,*poly_indsobj,*xxobj,*yyobj,*nclip_polyobj,*areasobj;
  if (!PyArg_ParseTuple(args, "OOOOOOOOOOOO",&lobj,&robj,&bobj,&tobj,&pxobj,&pyobj,&n_polyobj,&poly_indsobj,&xxobj,&yyobj,&nclip_polyobj,&areasobj)){
    return NULL;
  }

  PyObject *larr=NULL,*rarr=NULL,*barr=NULL,*tarr=NULL,*pxarr=NULL,*pyarr=NULL;
  PyObject *n_polyarr=NULL,*poly_indsarr=NULL,*xxarr=NULL,*yyarr=NULL;
  PyObject *nclip_polyarr=NULL,*areasarr=NULL;
  int *l,*r,*b,*t,*n_poly,*poly_inds,*xx,*yy,*nclip_poly;
  float *px,*py,*areas;
  int ok=0;

  /* if arrays, then extract them to objects. The output arrays are
     converted with writeback so that results always reach the caller. */
  if ((larr=PyArray_FROM_OTF(lobj,NPY_INT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((rarr=PyArray_FROM_OTF(robj,NPY_INT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((barr=PyArray_FROM_OTF(bobj,NPY_INT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((tarr=PyArray_FROM_OTF(tobj,NPY_INT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((pxarr=PyArray_FROM_OTF(pxobj,NPY_FLOAT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((pyarr=PyArray_FROM_OTF(pyobj,NPY_FLOAT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((n_polyarr=PyArray_FROM_OTF(n_polyobj,NPY_INT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((poly_indsarr=PyArray_FROM_OTF(poly_indsobj,NPY_INT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;
  if ((xxarr=PyArray_FROM_OTF(xxobj,NPY_INT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;
  if ((yyarr=PyArray_FROM_OTF(yyobj,NPY_INT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;
  if ((nclip_polyarr=PyArray_FROM_OTF(nclip_polyobj,NPY_INT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;
  if ((areasarr=PyArray_FROM_OTF(areasobj,NPY_FLOAT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;

  /* extract the array data to a C variable */
  l=(int*)PyArray_DATA((PyArrayObject*)larr);
  r=(int*)PyArray_DATA((PyArrayObject*)rarr);
  b=(int*)PyArray_DATA((PyArrayObject*)barr);
  t=(int*)PyArray_DATA((PyArrayObject*)tarr);
  px=(float*)PyArray_DATA((PyArrayObject*)pxarr);
  py=(float*)PyArray_DATA((PyArrayObject*)pyarr);
  n_poly=(int*)PyArray_DATA((PyArrayObject*)n_polyarr);
  poly_inds=(int*)PyArray_DATA((PyArrayObject*)poly_indsarr);
  xx=(int*)PyArray_DATA((PyArrayObject*)xxarr);
  yy=(int*)PyArray_DATA((PyArrayObject*)yyarr);
  nclip_poly=(int*)PyArray_DATA((PyArrayObject*)nclip_polyarr);
  areas=(float*)PyArray_DATA((PyArrayObject*)areasarr);

  /* call function */
  polyclip_multi(l,r,b,t,px,py,n_poly[0],poly_inds,xx,yy,nclip_poly,areas);
  ok=1;

 cleanup:
  /* clean up memory */
  Py_XDECREF(larr);
  Py_XDECREF(rarr);
  Py_XDECREF(barr);
  Py_XDECREF(tarr);
  Py_XDECREF(pxarr);
  Py_XDECREF(pyarr);
  Py_XDECREF(n_polyarr);
  if (release_array(poly_indsarr,ok) < 0) ok=0;
  if (release_array(xxarr,ok) < 0) ok=0;
  if (release_array(yyarr,ok) < 0) ok=0;
  if (release_array(nclip_polyarr,ok) < 0) ok=0;
  if (release_array(areasarr,ok) < 0) ok=0;

  if (!ok) return NULL;
  Py_RETURN_NONE;
}


static PyObject *py_single(PyObject *self,PyObject *args){
  /* Function to link to the polyclip_single function */

  /* Create objects from the inputs */
  PyObject *lobj,*robj,*bobj,*tobj,*nvertsobj;
  PyObject *pxobj,*pyobj,*px_outobj,*py_outobj,*areasobj;
  PyObject *indsobj,*nclip_polyobj,*ri_outobj;

  if(!PyArg_ParseTuple(args,"OOOOOOOOOOOOO",&lobj,&robj,&bobj,&tobj,&pxobj,&pyobj,&nvertsobj,&px_outobj,&py_outobj,&indsobj,&nclip_polyobj,&areasobj,&ri_outobj)){
    return NULL;
  }

  PyObject *larr=NULL,*rarr=NULL,*barr=NULL,*tarr=NULL,*nvertsarr=NULL;
  PyObject *pxarr=NULL,*pyarr=NULL,*px_outarr=NULL,*py_outarr=NULL;
  PyObject *areasarr=NULL,*indsarr=NULL,*nclip_polyarr=NULL,*ri_outarr=NULL;
  int *l,*r,*b,*t,*nverts,*inds,*nclip_poly,*ri_out;
  float *px,*py,*px_out,*py_out,*areas;
  int n,ok=0;

  /* if arrays, then extract them to objects. The output arrays are
     converted with writeback so that results always reach the caller. */
  if ((larr=PyArray_FROM_OTF(lobj,NPY_INT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((rarr=PyArray_FROM_OTF(robj,NPY_INT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((barr=PyArray_FROM_OTF(bobj,NPY_INT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((tarr=PyArray_FROM_OTF(tobj,NPY_INT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((nvertsarr=PyArray_FROM_OTF(nvertsobj,NPY_INT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((pxarr=PyArray_FROM_OTF(pxobj,NPY_FLOAT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((pyarr=PyArray_FROM_OTF(pyobj,NPY_FLOAT32,NPY_ARRAY_IN_ARRAY)) == NULL) goto cleanup;
  if ((px_outarr=PyArray_FROM_OTF(px_outobj,NPY_FLOAT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;
  if ((py_outarr=PyArray_FROM_OTF(py_outobj,NPY_FLOAT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;
  if ((areasarr=PyArray_FROM_OTF(areasobj,NPY_FLOAT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;
  if ((indsarr=PyArray_FROM_OTF(indsobj,NPY_INT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;
  if ((nclip_polyarr=PyArray_FROM_OTF(nclip_polyobj,NPY_INT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;
  if ((ri_outarr=PyArray_FROM_OTF(ri_outobj,NPY_INT32,NPY_ARRAY_INOUT_ARRAY2)) == NULL) goto cleanup;

  /* extract the array data to a C variable */
  l=(int*)PyArray_DATA((PyArrayObject*)larr);
  r=(int*)PyArray_DATA((PyArrayObject*)rarr);
  b=(int*)PyArray_DATA((PyArrayObject*)barr);
  t=(int*)PyArray_DATA((PyArrayObject*)tarr);
  nverts=(int*)PyArray_DATA((PyArrayObject*)nvertsarr);
  px=(float*)PyArray_DATA((PyArrayObject*)pxarr);
  py=(float*)PyArray_DATA((PyArrayObject*)pyarr);
  px_out=(float*)PyArray_DATA((PyArrayObject*)px_outarr);
  py_out=(float*)PyArray_DATA((PyArrayObject*)py_outarr);
  areas=(float*)PyArray_DATA((PyArrayObject*)areasarr);
  inds=(int*)PyArray_DATA((PyArrayObject*)indsarr);
  nclip_poly=(int*)PyArray_DATA((PyArrayObject*)nclip_polyarr);
  ri_out=(int*)PyArray_DATA((PyArrayObject*)ri_outarr);

  /* call function */
  n=nclip_poly[0];
  polyclip_single(l[0],r[0],b[0],t[0],px,py,nverts[0],inds,&n,areas,px_out,py_out,ri_out);
  nclip_poly[0]=n;
  ok=1;

 cleanup:
  /* clean up memory */
  Py_XDECREF(larr);
  Py_XDECREF(rarr);
  Py_XDECREF(barr);
  Py_XDECREF(tarr);
  Py_XDECREF(nvertsarr);
  Py_XDECREF(pxarr);
  Py_XDECREF(pyarr);
  if (release_array(px_outarr,ok) < 0) ok=0;
  if (release_array(py_outarr,ok) < 0) ok=0;
  if (release_array(areasarr,ok) < 0) ok=0;
  if (release_array(indsarr,ok) < 0) ok=0;
  if (release_array(nclip_polyarr,ok) < 0) ok=0;
  if (release_array(ri_outarr,ok) < 0) ok=0;

  if (!ok) return NULL;
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
  /* The clipping state in polyclip.c is thread-local, so the module
     can run without the GIL on free-threaded builds. */
  if (module != NULL && PyUnstable_Module_SetGIL(module, Py_MOD_GIL_NOT_USED) < 0) {
    Py_DECREF(module);
    return NULL;
  }
#endif
  return module;
}
