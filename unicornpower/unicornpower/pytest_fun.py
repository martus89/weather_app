import pytest


def sum_data(a, b):
  return a + b


def test_sum_data():
  x = 1
  y = 5
  result = sum_data(x,y)
  assert 6 == result

def test_sum_instance():
  x = 2
  y = 4
  assert isinstance(sum_data(x,y), int)

def multiply(c,d):
  return c*d

def test_multiply():
  x=6
  y=1
  assert multiply(x,y) == 6

def division(a,b):
  return a/b


@pytest.mark.parametrize("x,y,result", ((2, 2, 1), (-1, 4, -0.25)))
@pytest.mark.random_tag
def test_division(x,y,result):
  assert division(x,y) == result


@pytest.mark.random_tag
def test_division_zero_error():
  with pytest.raises(ZeroDivisionError):
    division(5, 0)


# pytest unicornpower/tests.py::test_division_zero_error

# pytest -k random_tag



@pytest.mark.random_tag
def testtwo_division():
  x = 6
  y = 2
  assert isinstance(division(x,y), float)


def insertex(x):
  if x==2:
    return True
  else:
    pass

def test_insertex():
  a=2
  assert insertex(a)


@pytest.mark.parametrize('param', (5, -5, -5000, 5000))
def test_insertex_return_none(param):
  assert insertex(param) is None


class BaseExp(Exception):
  pass

class FirstException(BaseExp):
  pass

class SecondException(BaseExp):
  pass

class ThirdException(BaseExp):
  pass


def foo(x):
  if x > 10:
    raise FirstException
  elif x == 10:
    raise SecondException
  else:
    raise ThirdException


@pytest.mark.parametrize("x, exception", ((11, FirstException), (10, SecondException), (-1, ThirdException)))
def test_foo(x, exception):
  with pytest.raises(exception):
    foo(x)


@pytest.mark.parametrize("x",(11,10,-1))
def test_foo_dont_care_about_exc_type(x):
  with pytest.raises(Exception):
    foo(x)
