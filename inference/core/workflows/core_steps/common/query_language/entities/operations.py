from typing import Any, List, Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from inference.core.workflows.core_steps.common.query_language.entities.enums import (
    DetectionsProperty,
    NumberCastingMode,
    SequenceAggregationFunction,
    SequenceAggregationMode,
    SequenceUnwrapMethod,
    StatementsGroupsOperator,
)
from inference.core.workflows.entities.types import (
    BOOLEAN_KIND,
    DETECTION_KIND,
    DICTIONARY_KIND,
    FLOAT_KIND,
    FLOAT_ZERO_TO_ONE_KIND,
    INSTANCE_SEGMENTATION_PREDICTION_KIND,
    INTEGER_KIND,
    KEYPOINT_DETECTION_PREDICTION_KIND,
    LIST_OF_VALUES_KIND,
    OBJECT_DETECTION_PREDICTION_KIND,
    STRING_KIND,
    WILDCARD_KIND,
)

TYPE_PARAMETER_NAME = "type"
DEFAULT_OPERAND_NAME = "_"


class OperationDefinition(BaseModel):
    type: str


class StringToLowerCase(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Executes lowercase operation on input string",
            "compound": False,
            "input_kind": [STRING_KIND],
            "output_kind": [STRING_KIND],
        },
    )
    type: Literal["StringToLowerCase"]


class StringToUpperCase(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Executes uppercase operation on input string",
            "compound": False,
            "input_kind": [STRING_KIND],
            "output_kind": [STRING_KIND],
        },
    )
    type: Literal["StringToUpperCase"]


class LookupTable(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Changes value according to mapping stated in lookup table",
            "compound": False,
            "input_kind": [WILDCARD_KIND],
            "output_kind": [WILDCARD_KIND],
        },
    )
    type: Literal["LookupTable"]
    lookup_table: dict


class ToNumber(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Changes value into number - float or int depending on configuration",
            "compound": False,
            "input_kind": [
                STRING_KIND,
                BOOLEAN_KIND,
                INTEGER_KIND,
                FLOAT_KIND,
                FLOAT_ZERO_TO_ONE_KIND,
            ],
            "output_kind": [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
        },
    )
    type: Literal["ToNumber"]
    cast_to: NumberCastingMode


class NumberRound(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Rounds the number",
            "compound": False,
            "input_kind": [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
            "output_kind": [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
        },
    )
    type: Literal["NumberRound"]
    decimal_digits: int


class SequenceMap(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Changes each value of sequence according to mapping stated in lookup table",
            "compound": True,
            "input_kind": [LIST_OF_VALUES_KIND],
            "output_kind": [LIST_OF_VALUES_KIND],
            "nested_operation_input_kind": [WILDCARD_KIND],
            "nested_operation_output_kind": [WILDCARD_KIND],
        },
    )
    type: Literal["SequenceMap"]
    lookup_table: dict


class NumericSequenceAggregate(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Aggregates numeric sequence using aggregation function like min or max - adjusted to work on numbers",
            "compound": False,
            "input_kind": [LIST_OF_VALUES_KIND],
            "output_kind": [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
        },
    )
    type: Literal["NumericSequenceAggregate"]
    function: SequenceAggregationFunction


class SequenceAggregate(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Aggregates sequence using generic aggregation methods - adjusted to majority data types",
            "compound": False,
            "input_kind": [LIST_OF_VALUES_KIND],
            "output_kind": [WILDCARD_KIND],
        },
    )
    type: Literal["SequenceAggregate"]
    mode: SequenceAggregationMode


class ToString(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Stringifies data",
            "compound": False,
            "input_kind": [WILDCARD_KIND],
            "output_kind": [STRING_KIND],
        },
    )
    type: Literal["ToString"]


class ToBoolean(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Changes input data into boolean",
            "compound": False,
            "input_kind": [FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND, INTEGER_KIND],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["ToBoolean"]


class StringSubSequence(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Takes sub-string of the input string",
            "compound": False,
            "input_kind": [STRING_KIND],
            "output_kind": [STRING_KIND],
        },
    )
    type: Literal["StringSubSequence"]
    start: int = Field(default=0)
    end: int = Field(default=-1)


class DetectionsPropertyExtract(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Extracts property from detections-based prediction"
            "(as a list of elements - one element represents single detection)",
            "compound": False,
            "input_kind": [
                OBJECT_DETECTION_PREDICTION_KIND,
                INSTANCE_SEGMENTATION_PREDICTION_KIND,
                KEYPOINT_DETECTION_PREDICTION_KIND,
            ],
            "output_kind": [LIST_OF_VALUES_KIND],
        },
    )
    type: Literal["DetectionsPropertyExtract"]
    property_name: DetectionsProperty


class ExtractDetectionProperty(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Extracts property from single detection",
            "compound": False,
            "input_kind": [DETECTION_KIND],
            "output_kind": [WILDCARD_KIND],
        },
    )
    type: Literal["ExtractDetectionProperty"]
    property_name: DetectionsProperty
    unwrap_method: SequenceUnwrapMethod = SequenceUnwrapMethod.FIRST


class DetectionsFilter(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Filters out unwanted elements from detections-based prediction by "
            "applying filter operation in context of every single detection within prediction",
            "compound": True,
            "input_kind": [
                OBJECT_DETECTION_PREDICTION_KIND,
                INSTANCE_SEGMENTATION_PREDICTION_KIND,
                KEYPOINT_DETECTION_PREDICTION_KIND,
            ],
            "output_kind": [
                OBJECT_DETECTION_PREDICTION_KIND,
                INSTANCE_SEGMENTATION_PREDICTION_KIND,
                KEYPOINT_DETECTION_PREDICTION_KIND,
            ],
            "nested_operation_input_kind": [DETECTION_KIND],
            "nested_operation_output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["DetectionsFilter"]
    filter_operation: "StatementGroup"


class DetectionsOffset(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Makes detected bounding boxes bigger by applying offset to its size",
            "compound": False,
            "input_kind": [
                OBJECT_DETECTION_PREDICTION_KIND,
                INSTANCE_SEGMENTATION_PREDICTION_KIND,
                KEYPOINT_DETECTION_PREDICTION_KIND,
            ],
            "output_kind": [
                OBJECT_DETECTION_PREDICTION_KIND,
                INSTANCE_SEGMENTATION_PREDICTION_KIND,
                KEYPOINT_DETECTION_PREDICTION_KIND,
            ],
        },
    )
    type: Literal["DetectionsOffset"]
    offset_x: int
    offset_y: int


class DetectionsShift(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Shifting detected bounding boxes in assigned direction",
            "compound": False,
            "input_kind": [
                OBJECT_DETECTION_PREDICTION_KIND,
                INSTANCE_SEGMENTATION_PREDICTION_KIND,
                KEYPOINT_DETECTION_PREDICTION_KIND,
            ],
            "output_kind": [
                OBJECT_DETECTION_PREDICTION_KIND,
                INSTANCE_SEGMENTATION_PREDICTION_KIND,
                KEYPOINT_DETECTION_PREDICTION_KIND,
            ],
        },
    )
    type: Literal["DetectionsShift"]
    shift_x: int
    shift_y: int


class RandomNumber(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Special operation to let random sampling - ignoring input data and changing it "
            "into random floating point value. To be used mainly to sample predictions or images.",
            "input_kind": [
                OBJECT_DETECTION_PREDICTION_KIND,
                INSTANCE_SEGMENTATION_PREDICTION_KIND,
                KEYPOINT_DETECTION_PREDICTION_KIND,
                WILDCARD_KIND,
            ],
            "output_kind": [FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
        },
    )
    type: Literal["RandomNumber"]
    min_value: float = Field(default=0.0)
    max_value: float = Field(default=1.0)


class StringMatches(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if string matches regex",
            "compound": False,
            "input_kind": [STRING_KIND],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["StringMatches"]
    regex: str


class SequenceLength(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Operation determines the length of input sequence",
            "compound": False,
            "input_kind": [
                OBJECT_DETECTION_PREDICTION_KIND,
                INSTANCE_SEGMENTATION_PREDICTION_KIND,
                KEYPOINT_DETECTION_PREDICTION_KIND,
                LIST_OF_VALUES_KIND,
                DICTIONARY_KIND,
            ],
            "output_kind": [INTEGER_KIND],
        },
    )
    type: Literal["SequenceLength"]


class SequenceApply(OperationDefinition):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Operation applies chain of operations at every element of sequence",
            "compound": True,
            "input_kind": [LIST_OF_VALUES_KIND],
            "output_kind": [LIST_OF_VALUES_KIND],
            "nested_operation_input_kind": [WILDCARD_KIND],
            "nested_operation_output_kind": [WILDCARD_KIND],
        },
    )
    type: Literal["SequenceApply"]
    operations: List["AllOperationsType"]


AllOperationsType = Annotated[
    Union[
        StringToLowerCase,
        StringToUpperCase,
        LookupTable,
        ToNumber,
        NumberRound,
        SequenceMap,
        SequenceApply,
        NumericSequenceAggregate,
        ToString,
        ToBoolean,
        StringSubSequence,
        DetectionsPropertyExtract,
        SequenceAggregate,
        ExtractDetectionProperty,
        DetectionsFilter,
        DetectionsOffset,
        DetectionsShift,
        RandomNumber,
        StringMatches,
        SequenceLength,
    ],
    Field(discriminator="type"),
]


class OperationsChain(BaseModel):
    operations: List[AllOperationsType]


class BinaryOperator(BaseModel):
    type: str


class Equals(BinaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if two values given are equal",
            "operands_number": 2,
            "operands_kinds": [
                [
                    INTEGER_KIND,
                    STRING_KIND,
                    FLOAT_KIND,
                    FLOAT_ZERO_TO_ONE_KIND,
                    BOOLEAN_KIND,
                ],
                [
                    INTEGER_KIND,
                    STRING_KIND,
                    FLOAT_KIND,
                    FLOAT_ZERO_TO_ONE_KIND,
                    BOOLEAN_KIND,
                ],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["=="]


class NotEquals(BinaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if two values given are not equal",
            "operands_number": 2,
            "operands_kinds": [
                [
                    INTEGER_KIND,
                    STRING_KIND,
                    FLOAT_KIND,
                    FLOAT_ZERO_TO_ONE_KIND,
                    BOOLEAN_KIND,
                ],
                [
                    INTEGER_KIND,
                    STRING_KIND,
                    FLOAT_KIND,
                    FLOAT_ZERO_TO_ONE_KIND,
                    BOOLEAN_KIND,
                ],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["!="]


class NumerGreater(BinaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if first value (number) is greater than the second value (number)",
            "operands_number": 2,
            "operands_kinds": [
                [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
                [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(Number) >"]


class NumerGreaterEqual(BinaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if first value (number) is greater or equal than the second value (number)",
            "operands_number": 2,
            "operands_kinds": [
                [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
                [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(Number) >="]


class NumerLower(BinaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if first value (number) is lower than the second value (number)",
            "operands_number": 2,
            "operands_kinds": [
                [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
                [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(Number) <"]


class NumerLowerEqual(BinaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if first value (number) is lower or equal than the second value (number)",
            "operands_number": 2,
            "operands_kinds": [
                [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
                [INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(Number) <="]


class StringStartsWith(BinaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if string given as first value starts with string provided as second value",
            "operands_number": 2,
            "operands_kinds": [
                [STRING_KIND],
                [STRING_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(String) startsWith"]


class StringEndsWith(BinaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if string given as first value ends with string provided as second value",
            "operands_number": 2,
            "operands_kinds": [
                [STRING_KIND],
                [STRING_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(String) endsWith"]


class StringContains(BinaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if string given as first value contains string provided as second value",
            "operands_number": 2,
            "operands_kinds": [
                [STRING_KIND],
                [STRING_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(String) contains"]


class In(BinaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if first value is element of second value (usually list or dictionary)",
            "operands_number": 2,
            "operands_kinds": [
                [STRING_KIND, INTEGER_KIND, FLOAT_KIND, FLOAT_ZERO_TO_ONE_KIND],
                [LIST_OF_VALUES_KIND, DICTIONARY_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["in"]


class UnaryOperator(BaseModel):
    type: str


class Exists(UnaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if value is given (not `None`)",
            "operands_number": 1,
            "operands_kinds": [
                [WILDCARD_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["Exists"]


class DoesNotExist(UnaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if value is not given (`None`)",
            "operands_number": 1,
            "operands_kinds": [
                [WILDCARD_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["DoesNotExist"]


class IsTrue(UnaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if value is `True`",
            "operands_number": 1,
            "operands_kinds": [
                [BOOLEAN_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(Boolean) is True"]


class IsFalse(UnaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if value is `False`",
            "operands_number": 1,
            "operands_kinds": [
                [BOOLEAN_KIND],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(Boolean) is False"]


class IsEmpty(UnaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if sequence is empty",
            "operands_number": 1,
            "operands_kinds": [
                [
                    LIST_OF_VALUES_KIND,
                    DICTIONARY_KIND,
                    OBJECT_DETECTION_PREDICTION_KIND,
                    INSTANCE_SEGMENTATION_PREDICTION_KIND,
                    KEYPOINT_DETECTION_PREDICTION_KIND,
                ],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(Sequence) is empty"]


class IsNotEmpty(UnaryOperator):
    model_config = ConfigDict(
        json_schema_extra={
            "description": "Checks if sequence is not empty",
            "operands_number": 1,
            "operands_kinds": [
                [
                    LIST_OF_VALUES_KIND,
                    DICTIONARY_KIND,
                    OBJECT_DETECTION_PREDICTION_KIND,
                    INSTANCE_SEGMENTATION_PREDICTION_KIND,
                    KEYPOINT_DETECTION_PREDICTION_KIND,
                ],
            ],
            "output_kind": [BOOLEAN_KIND],
        },
    )
    type: Literal["(Sequence) is not empty"]


class StaticOperand(BaseModel):
    type: Literal["StaticOperand"]
    value: Any
    operations: List["AllOperationsType"] = Field(default_factory=lambda: [])


class DynamicOperand(BaseModel):
    type: Literal["DynamicOperand"]
    operations: List["AllOperationsType"] = Field(default_factory=lambda: [])
    operand_name: str = DEFAULT_OPERAND_NAME


class BinaryStatement(BaseModel):
    type: Literal["BinaryStatement"]
    left_operand: Annotated[
        Union[StaticOperand, DynamicOperand], Field(discriminator="type")
    ]
    comparator: Annotated[
        Union[
            In,
            StringContains,
            StringEndsWith,
            StringStartsWith,
            NumerLowerEqual,
            NumerLower,
            NumerGreaterEqual,
            NumerGreater,
            NotEquals,
            Equals,
        ],
        Field(discriminator="type"),
    ]
    right_operand: Annotated[
        Union[StaticOperand, DynamicOperand], Field(discriminator="type")
    ]
    negate: bool = False


class UnaryStatement(BaseModel):
    type: Literal["UnaryStatement"]
    operand: Annotated[
        Union[StaticOperand, DynamicOperand], Field(discriminator="type")
    ]
    operator: Annotated[
        Union[Exists, DoesNotExist, IsTrue, IsFalse, IsEmpty, IsNotEmpty],
        Field(discriminator="type"),
    ]
    negate: bool = False


class StatementGroup(BaseModel):
    type: Literal["StatementGroup"]
    statements: List[
        Annotated[
            Union[BinaryStatement, UnaryStatement, "StatementGroup"],
            Field(discriminator="type"),
        ]
    ] = Field(min_items=1)
    operator: StatementsGroupsOperator = StatementsGroupsOperator.OR
