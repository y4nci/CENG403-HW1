import random
import math
from typing import Union

class gergen:
    pass

######################################################################
#------------------------- HELPER FUNCTIONS -------------------------#
######################################################################
def create_nested_list(boyut: tuple, aralik_list: list, current_dimension_idx: int, use_integer: bool) -> list:
    current_dimension = boyut[current_dimension_idx]

    if current_dimension == 0:
        raise ValueError('Dimension should be greater than 0')

    if current_dimension_idx == len(boyut) - 1:
        return [
            random.randint(*aralik_list) if use_integer else random.uniform(*aralik_list)
                for _ in range(current_dimension)
        ]
    
    return [create_nested_list(boyut, aralik_list, current_dimension_idx + 1, use_integer) for _ in range(current_dimension)]


def get_transpose_of_nested_list(nested_list: list | int | float) -> list | int | float:
    if (
        type(nested_list) == int or
        type(nested_list) == float or
        type(nested_list[0]) == int or
        type(nested_list[0]) == float
    ):
        return nested_list
    
    return [
        get_transpose_of_nested_list(
            [nested_list[i][j] for i in range(len(nested_list))]
        ) for j in range(len(nested_list[0]))
    ]


def get_dimensions_of_nested_list(nested_list: list) -> tuple:
    if type(nested_list) == int or type(nested_list) == float:
        return ()

    boyut_list = []
    current_nested_list = nested_list

    while type(current_nested_list[0]) != int and type(current_nested_list[0]) != float:
        boyut_list.append(len(current_nested_list))
        current_nested_list = current_nested_list[0]

    boyut_list.append(len(current_nested_list))

    return tuple(boyut_list)


def unnest_list(nested_list: list) -> list:
    if (
        type(nested_list) == int or
        type(nested_list) == float
    ):
        return [nested_list]
    
    return [
        el for sublist in nested_list for el in unnest_list(sublist)
    ]


def nest_list(unnested_list: list, boyut: tuple) -> list:
    if len(boyut) == 0:
        return unnested_list[0]

    if isinstance(unnested_list, (int, float)):
        return unnested_list
    
    prod = 1

    for el in boyut[1:]:
        prod *= el

    return [
        nest_list(unnested_list[i:i+prod], boyut[1:]) for i in range(boyut[0])
    ]


def map_nested_list(nested_list: list, map_fn) -> list:
    if (
        type(nested_list) == int or
        type(nested_list) == float
    ):
        return map_fn(nested_list)
    
    return [
        map_nested_list(el, map_fn) for el in nested_list
    ]


######################################################################
#-------------------- FUNDAMENTAL FUNCTIONALITIES -------------------#
######################################################################
def cekirdek(sayi: int) -> None:
    """
    Sets the seed for random number generation to ensure reproducibility of results. Before generating random numbers (for instance,
    when initializing tensors with random values), you can call this function to set the seed.
    """
    random.seed(sayi)


def rastgele_dogal(boyut: tuple, aralik: tuple = (0, 100), dagilim='uniform') -> gergen:
    """
    Generates a gergen of specified dimensions with random integer values. The boyut parameter is a tuple specifying the dimensions of
    the gergen to be generated. The aralik parameter is an optional tuple (min, max) specifying the range of random values, with a 
    default range of (0, 100). The dagilim parameter specifies the distribution of random values, with ‘uniform’ as the default
    distribution. Possible values for dagilim include ‘uniform’ for a uniform distribution. You should raise ValueError if dagilim
    parameter is given differently.
    """

    if dagilim != 'uniform':
        raise ValueError('dagilim parameter should be uniform')
    
    aralik_list: list = list(aralik)

    # if boyut is 0, then we should return a scalar.
    if len(boyut) == 0:
        random_scalar = random.randint(*aralik_list)

        return gergen(random_scalar)

    return gergen(create_nested_list(boyut, aralik_list, 0, True))


def rastgele_gercek(boyut: tuple, aralik: tuple = (0.0,1.0), dagilim = None) -> gergen:
    """
    Generates a gergen of specified dimensions with random floating-point values. The boyut parameter is a tuple specifying the dimensions
    of the gergen to be generated. The aralik parameter is an optional tuple (min, max) specifying the range of random values, with a
    default range of (0.0,1.0). The dagilim parameter specifies the distribution of random values, with ‘uniform’ as the default
    distribution. Possible values for dagilim include ‘uniform’ for a uniform distribution. You should raise ValueError if dagilim
    parameter is given differently.
    """

    if dagilim != 'uniform':
        raise ValueError('dagilim parameter should be uniform')
    
    aralik_list: list = list(aralik)

    # if boyut is 0, then we should return a scalar.
    if len(boyut) == 0:
        random_scalar = random.uniform(*aralik_list)

        return gergen(random_scalar)
    
    return gergen(create_nested_list(boyut, aralik_list, 0, False))


######################################################################
#------------------------ OPERATION CLASSES -------------------------#
######################################################################

class Operation:
    def __call__(self, *operands):
        """
        Makes an instance of the Operation class callable.
        Stores operands and initializes outputs to None.
        Invokes the forward pass of the operation with given operands.

        Parameters:
            *operands: Variable length operand list.

        Returns:
            The result of the forward pass of the operation.
        """
        self.operands = operands
        self.outputs = None
        return self.ileri(*operands)

    def ileri(self, *operands):
        """
        Defines the forward pass of the operation.
        Must be implemented by subclasses to perform the actual operation.

        Parameters:
            *operands: Variable length operand list.

        Raises:
            NotImplementedError: If not overridden in a subclass.
        """
        raise NotImplementedError


"""
The Operation class serves as a base class for operations in the gergen class. It is defined as above.

The call method allows instances of subclasses of Operation to be used as if they were functions, enabling a concise syntax for applying
operations to operands. The ileri method is intended to be overridden by subclasses to define the specific behavior of the operation.
In the context of the gergen class, the Operation class serves as a foundational component for defining various mathematical and tensor
operations. When creating new operations, such as addition, multiplication, or more complex functions, you should define subclasses of
Operation and implement the ileri method to encapsulate the operation’s specific logic. The call method in the Operation base class will
automatically handle the invocation of the ileri method, treating instances of these subclasses as callable objects. To integrate an
operation into the gergen class, instantiate the corresponding Operation subclass and pass the necessary operands (other gergen instances
or scalars) to perform the operation, ultimately returning a new gergen object that represents the result.
"""


class Addition(Operation):
    def adder(self, left: Union[list, int, float], right: Union[list, int, float]) -> Union[list, int, float]:
        """
        For gergen-to-gergen addition, it iterates over corresponding el- ements from both instances, adding them together. If one
        operand is a scalar, this value is added to every element within the gergen instance. The method performs a dimensionality
        check when both operands are gergen instances to ensure their shapes are compatible for element-wise operations. If the
        dimensions do not align, a ValueError is raised, indicating a mismatch in dimensions. Additionally, if the other parameter is
        of an unsupported type, a TypeError is raised to maintain type safety. The outcome of the addition is should be returned in a 
        new gergen object.
        """
        if (
            isinstance(left, (list)) and
            isinstance(right, (list))
        ):
            """
            both gergos (represented by lists)
            """
            
            return ([
                self.adder(
                    left[i],
                    right[i]
                ) for i in range(len(left))
            ])
        
        if (
            isinstance(left, (int, float)) and
            isinstance(right, (int, float))
        ):
            """
            both scalars
            """
            return left + right
        
        if isinstance(left, (int, float)):
            """
            left is scalar
            """
            return ([
                self.adder(left, el) for el in right
            ])

        if isinstance(right, (int, float)):
            """
            right is scalar
            """
            return ([
                self.adder(el, right) for el in left
            ])
        
        raise TypeError('Operands should be of type int, float, or gergen')

    def ileri(self, *operands: Union['gergen', int, float]) -> 'gergen':
        """
        Defines the forward pass of the addition operation.
        Adds the given operands element-wise.

        Parameters:
            *operands: Variable length operand list.

        Returns:
            The result of the addition operation.
        """
        if not all(isinstance(operand, (int, float, gergen)) for operand in operands):
            raise TypeError('Operands should be of type int, float, or gergen')

        if len(operands) < 2:
            raise ValueError('Addition operation requires at least two operands')
        
        if len(operands) == 2:
            if (
                isinstance(operands[0], (gergen)) and
                isinstance(operands[1], (gergen))
            ):
                if operands[0].boyut() != operands[1].boyut():
                    raise ValueError('Operands should have the same shape')

            #! WE WILL NOT USE THE GERGEN OBJECT IN adder FUNCTION. INSTEAD, WE WILL PASS THE listeye() OF THE GERGEN OBJECT.
            neutralised_operands = [
                operand if isinstance(operand, (int, float)) else operand.listeye()
                    for operand in operands
            ]

            #! WE WILL RETURN THE RESULT AS A GERGEN OBJECT.
            return gergen(self.adder(*neutralised_operands))

        result = operands[0]

        result = self(result, operands[1:])

        return result


class Subtraction(Operation):
    def subtractor(self, left: Union[list, int, float], right: Union[list, int, float]) -> Union[list, int, float]:
        """
        For gergen-to-gergen addition, it iterates over corresponding el- ements from both instances, adding them together. If one
        operand is a scalar, this value is added to every element within the gergen instance. The method performs a dimensionality
        check when both operands are gergen instances to ensure their shapes are compatible for element-wise operations. If the
        dimensions do not align, a ValueError is raised, indicating a mismatch in dimensions. Additionally, if the other parameter is
        of an unsupported type, a TypeError is raised to maintain type safety. The outcome of the addition is should be returned in a 
        new gergen object.
        """
        if (
            isinstance(left, (list)) and
            isinstance(right, (list))
        ):
            """
            both gergos (represented by lists)
            """
            
            return ([
                self.subtractor(
                    left[i],
                    right[i]
                ) for i in range(len(left))
            ])
        
        if (
            isinstance(left, (int, float)) and
            isinstance(right, (int, float))
        ):
            """
            both scalars
            """
            return left - right
        
        if isinstance(left, (int, float)):
            """
            left is scalar
            """
            return ([
                self.subtractor(left, el) for el in right
            ])

        if isinstance(right, (int, float)):
            """
            right is scalar
            """
            return ([
                self.subtractor(el, right) for el in left
            ])
        
        raise TypeError('Operands should be of type int, float, or gergen')

    def ileri(self, *operands: Union['gergen', int, float]) -> 'gergen':
        """
        Defines the forward pass of the addition operation.
        Adds the given operands element-wise.

        Parameters:
            *operands: Variable length operand list.

        Returns:
            The result of the addition operation.
        """
        if not all(isinstance(operand, (int, float, gergen)) for operand in operands):
            raise TypeError('Operands should be of type int, float, or gergen')

        if len(operands) < 2:
            raise ValueError('Addition operation requires at least two operands')
        
        if len(operands) == 2:
            if (
                isinstance(operands[0], (gergen)) and
                isinstance(operands[1], (gergen))
            ):
                if operands[0].boyut() != operands[1].boyut():
                    raise ValueError('Operands should have the same shape')

            #! WE WILL NOT USE THE GERGEN OBJECT IN adder FUNCTION. INSTEAD, WE WILL PASS THE listeye() OF THE GERGEN OBJECT.
            neutralised_operands = [
                operand if isinstance(operand, (int, float)) else operand.listeye()
                    for operand in operands
            ]

            #! WE WILL RETURN THE RESULT AS A GERGEN OBJECT.
            return gergen(self.subtractor(*neutralised_operands))

        result = operands[0]

        result = self(result, operands[1:])

        return result
    

class Multiplication(Operation):
    def multiplier(self, left, right):
        """
        This method fa- cilitates the multiplication of the gergen either with another gergen instance for element-wise multiplication,
        or with a scalar (int/float), yielding a new gergen ob- ject as the result. The other parameter is permitted to be a gergen, an
        integer, or a floating-point number. Error handling is incorporated to manage cases where the other parameter is neither a gergen
        object nor a numerical scalar. If the dimen- sions of two gergen instances do not align for element-wise multiplication, or if an
        incompatible type is provided for other, a TypeError or ValueError is raised.
        """
        if (
            isinstance(left, (list)) and
            isinstance(right, (list))
        ):
            """
            both gergos (represented by lists)
            """
            
            return ([
                self.multiplier(
                    left[i],
                    right[i]
                ) for i in range(len(left))
            ])
        
        if (
            isinstance(left, (int, float)) and
            isinstance(right, (int, float))
        ):
            """
            both scalars
            """
            return left * right
        
        if isinstance(left, (int, float)):
            """
            left is scalar
            """
            return ([
                self.multiplier(left, el) for el in right
            ])

        if isinstance(right, (int, float)):
            """
            right is scalar
            """
            return ([
                self.multiplier(el, right) for el in left
            ])
        
        raise TypeError('Operands should be of type int, float, or gergen')

    def ileri(self, *operands: Union['gergen', int, float]) -> 'gergen':
        """
        Defines the forward pass of the addition operation.
        Adds the given operands element-wise.

        Parameters:
            *operands: Variable length operand list.

        Returns:
            The result of the addition operation.
        """
        if not all(isinstance(operand, (int, float, gergen)) for operand in operands):
            raise TypeError('Operands should be of type int, float, or gergen')

        if len(operands) < 2:
            raise ValueError('Multiplication operation requires at least two operands')
        
        if len(operands) == 2:
            if (
                isinstance(operands[0], (gergen)) and
                isinstance(operands[1], (gergen))
            ):
                if operands[0].boyut() != operands[1].boyut():
                    raise ValueError('Operands should have the same shape')

            #! WE WILL NOT USE THE GERGEN OBJECT IN adder FUNCTION. INSTEAD, WE WILL PASS THE listeye() OF THE GERGEN OBJECT.
            neutralised_operands = [
                operand if isinstance(operand, (int, float)) else operand.listeye()
                    for operand in operands
            ]

            #! WE WILL RETURN THE RESULT AS A GERGEN OBJECT.
            return gergen(self.multiplier(*neutralised_operands))

        result = operands[0]

        result = self(result, operands[1:])

        return result
            

class Division(Operation):
    def divisor(self, left, right):
        """
        This method fa- cilitates the multiplication of the gergen either with another gergen instance for element-wise multiplication,
        or with a scalar (int/float), yielding a new gergen ob- ject as the result. The other parameter is permitted to be a gergen, an
        integer, or a floating-point number. Error handling is incorporated to manage cases where the other parameter is neither a gergen
        object nor a numerical scalar. If the dimen- sions of two gergen instances do not align for element-wise multiplication, or if an
        incompatible type is provided for other, a TypeError or ValueError is raised.
        """
        if (
            isinstance(left, (list)) and
            isinstance(right, (list))
        ):
            """
            both gergos (represented by lists)
            """
            
            return ([
                self.divisor(
                    left[i],
                    right[i]
                ) for i in range(len(left))
            ])
        
        if (
            isinstance(left, (int, float)) and
            isinstance(right, (int, float))
        ):
            """
            both scalars
            """
            return left / right
        
        if isinstance(left, (int, float)):
            """
            left is scalar
            """
            return ([
                self.divisor(left, el) for el in right
            ])

        if isinstance(right, (int, float)):
            """
            right is scalar
            """
            return ([
                self.divisor(el, right) for el in left
            ])
        
        raise TypeError('Operands should be of type int, float, or gergen')

    def ileri(self, *operands: Union['gergen', int, float]) -> 'gergen':
        """
        Defines the forward pass of the addition operation.
        Adds the given operands element-wise.

        Parameters:
            *operands: Variable length operand list.

        Returns:
            The result of the addition operation.
        """
        if not all(isinstance(operand, (int, float, gergen)) for operand in operands):
            raise TypeError('Operands should be of type int, float, or gergen')

        if len(operands) < 2:
            raise ValueError('Multiplication operation requires at least two operands')
        
        if len(operands) == 2:
            if (
                isinstance(operands[0], (gergen)) and
                isinstance(operands[1], (gergen))
            ):
                if operands[0].boyut() != operands[1].boyut():
                    raise ValueError('Operands should have the same shape')

            #! WE WILL NOT USE THE GERGEN OBJECT IN adder FUNCTION. INSTEAD, WE WILL PASS THE listeye() OF THE GERGEN OBJECT.
            neutralised_operands = [
                operand if isinstance(operand, (int, float)) else operand.listeye()
                    for operand in operands
            ]

            #! WE WILL RETURN THE RESULT AS A GERGEN OBJECT.
            return gergen(self.divisor(*neutralised_operands))

        result = operands[0]

        result = self(result, operands[1:])

        return result


######################################################################
#------------------------- GERGOOOOOOOOOOOO -------------------------#
######################################################################

class gergen:

    __veri = None #A nested list of numbers representing the data
    D = None # Transpose of data
    __boyut = None #Dimensions of the derivative (Shape)

    __adder = Addition()
    __subtractor = Subtraction()
    __multiplier = Multiplication()
    __divider = Division()


    def __init__(self, veri=None):
    # The constructor for the 'gergen' class.
    #
    # This method initializes a new instance of a gergen object. The gergen can be
    # initialized with data if provided; otherwise, it defaults to None, representing
    # an empty tensor.
    #
    # Parameters:
    # veri (int/float, list, list of lists, optional): A nested list of numbers that represents the
    # gergen data. The outer list contains rows, and each inner list contains the
    # elements of each row. If 'veri' is None, the tensor is initialized without data.
    #
    # Example:
    # To create a tensor with data, pass a nested list:
    # tensor = gergen([[1, 2, 3], [4, 5, 6]])
    #
    # To create an empty tensor, simply instantiate the class without arguments:
    # empty_tensor = gergen()
        self.__veri = veri
        self.D = get_transpose_of_nested_list(veri)
        self.__boyut = get_dimensions_of_nested_list(veri)

    def __getitem__(self, index) -> gergen:
    #Indexing for gergen objects
        if self.__veri is None:
            raise ValueError('Tensor is empty')
        
        if type(index) == int:
            return gergen(self.__veri[index])
        
        if type(index) == tuple:
            val_to_return = self.__veri

            while len(index) > 0:
                val_to_return = val_to_return[index[0]]
                index = index[1:]

            return gergen(val_to_return)

    def __str__(self):
        #Generates a string representation
        string_to_print = ""

        if self.__veri is None:
            string_to_print += "Boş gergen"

        elif type(self.__veri) == int or type(self.__veri) == float:
            # If the tensor is a scalar, we can directly return the string representation of the scalar.
            string_to_print += "0 boyutlu skaler gergen:\n" + str(self.__veri)

        else:
            # If the tensor is not a scalar, we can make use of __boyut variable to construct a string representation.
            for dim in self.__boyut:
                string_to_print += str(dim) + "x"

            string_to_print = string_to_print[:-1]
            string_to_print += " boyutlu gergen:\n" + str(self.__veri)

        return string_to_print + "\n"


    def __mul__(self, other: Union['gergen', int, float]) -> 'gergen':
        """
        Multiplication operation for gergen objects.
        Called when a gergen object is multiplied by another, using the '*' operator.
        Could be element-wise multiplication or scalar multiplication, depending on the context.
        """
        return self.__multiplier(self, other)

    def __truediv__(self, other: Union['gergen', int, float]) -> 'gergen':
        """
        Division operation for gergen objects.
        Called when a gergen object is divided by another, using the '/' operator.
        The operation is element-wise.
        """
        return self.__divider(self, other)


    def __add__(self, other: Union['gergen', int, float]) -> 'gergen':
        """
        Defines the addition operation for gergen objects.
        Called when a gergen object is added to another, using the '+' operator.
        The operation is element-wise.
        """
        return self.__adder(self, other)

    def __sub__(self, other: Union['gergen', int, float]) -> 'gergen':
        """
        Subtraction operation for gergen objects.
        Called when a gergen object is subtracted from another, using the '-' operator.
        The operation is element-wise.
        """
        return self.__subtractor(self, other)

    def uzunluk(self):
    # Returns the total number of elements in the gergen
        if type(self.__veri) == int or type(self.__veri) == float:
            return 1
        
        return len(unnest_list(self.__veri))
        

    def boyut(self):
    # Returns the shape of the gergen
        return self.__boyut

    def devrik(self):
    # Returns the transpose of gergen
        return gergen(self.D)

    def sin(self):
    #Calculates the sine of each element in the given `gergen`.
        return gergen(map_nested_list(self.__veri, lambda x: math.sin(x)))

    def cos(self):
    #Calculates the cosine of each element in the given `gergen`.
        return gergen(map_nested_list(self.__veri, lambda x: math.cos(x)))

    def tan(self):
    #Calculates the tangent of each element in the given `gergen`.
        return gergen(map_nested_list(self.__veri, lambda x: math.tan(x)))

    def us(self, n: int):
    #Raises each element of the gergen object to the power 'n'. This is an element-wise operation.
        return gergen(map_nested_list(self.__veri, lambda x: x ** n))

    def log(self):
    #Applies the logarithm function to each element of the gergen object, using the base 10.
        return gergen(map_nested_list(self.__veri, lambda x: math.log(x, 10)))

    def ln(self):
    #Applies the natural logarithm function to each element of the gergen object.
        return gergen(map_nested_list(self.__veri, lambda x: math.log(x)))

    def L1(self):
    # Calculates and returns the L1 norm
        return self.Lp(1)

    def L2(self):
    # Calculates and returns the L2 norm
        return self.Lp(2)

    def Lp(self, p):
    # Calculates and returns the Lp norm, where p should be positive integer
        if p <= 0:
            raise ValueError('p should be a positive integer')

        unnested_list = unnest_list(self.__veri)

        return sum([abs(el) ** p for el in unnested_list]) ** (1 / p)

        pass

    def listeye(self):
    #Converts the gergen object into a list or a nested list, depending on its dimensions.
        return self.__veri

    def duzlestir(self):
    #Converts the gergen object's multi-dimensional structure into a 1D structure, effectively 'flattening' the object.
        return unnest_list(self.__veri)

    def boyutlandir(self, yeni_boyut):
    #Reshapes the gergen object to a new shape 'yeni_boyut', which is specified as a tuple.
        if not isinstance(yeni_boyut, tuple):
            raise ValueError('yeni_boyut should be a tuple')
        
        current_uzunluk = self.uzunluk()
        yeni_uzunluk = 1

        for dim in yeni_boyut:
            yeni_uzunluk *= dim

        if yeni_uzunluk != current_uzunluk:
            raise ValueError('The new shape should have the same number of elements as the original shape')

        unnested_list = unnest_list(self.__veri)

        return gergen(nest_list(unnested_list, yeni_boyut))

    def ic_carpim(self, other):
    #Calculates the inner (dot) product of this gergen object with another.
        pass

    def dis_carpim(self, other):
    #Calculates the outer product of this gergen object with another.
        pass
    def topla(self, eksen=None):
    #Sums up the elements of the gergen object, optionally along a specified axis 'eksen'.
        pass

    def ortalama(self, eksen=None):
    #Calculates the average of the elements of the gergen object, optionally along a specified axis 'eksen'.
        pass


    





















