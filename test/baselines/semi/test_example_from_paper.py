from itertools import zip_longest
from unittest import TestCase

from veniq.ast_framework import AST, ASTNodeType
from veniq.baselines.semi.extract_semantic import extract_method_statements_semantic, StatementSemantic
from veniq.baselines.semi.create_extraction_opportunities import create_extraction_opportunities
from veniq.baselines.semi.filter_extraction_opportunities import filter_extraction_opportunities
from .utils import get_method_ast, objects_semantic


class PaperExampleTestCase(TestCase):
    def test_semantic_extraction(self):
        method_ast = self._get_method_ast()
        semantic = extract_method_statements_semantic(method_ast)
        for comparison_index, (statement, actual_semantic, expected_semantic) in enumerate(
            zip_longest(semantic.keys(), semantic.values(), self._method_semantic)
        ):
            self.assertEqual(
                actual_semantic,
                expected_semantic,
                f"Failed on {statement.node_type} statement on line {statement.line}. "
                f"Comparison index is {comparison_index}.",
            )

    def test_extraction_opportunities_creation(self):
        method_ast = self._get_method_ast()
        semantic = extract_method_statements_semantic(method_ast)
        extraction_opportunities = create_extraction_opportunities(semantic)

        for opportunity_index, (actual_opportunity, expected_opportunity) in enumerate(
            zip_longest(extraction_opportunities, self._expected_extraction_opportunities)
        ):
            actual_opportunity_statement_types = [statement.node_type for statement in actual_opportunity]
            self.assertEqual(
                actual_opportunity_statement_types,
                expected_opportunity,
                f"Failed on {opportunity_index}th opportunity comparison",
            )

    def test_extraction_opportunities_filtering(self):
        method_ast = self._get_method_ast()
        semantic = extract_method_statements_semantic(method_ast)
        extraction_opportunities = create_extraction_opportunities(semantic)
        filtered_extraction_opportunities = filter_extraction_opportunities(
            extraction_opportunities, semantic, method_ast
        )

        for opportunity_index, (actual_opportunity, expected_opportunity) in enumerate(
            zip_longest(filtered_extraction_opportunities, self._expected_filtered_extraction_opportunities)
        ):
            actual_opportunity_statement_types = [statement.node_type for statement in actual_opportunity]
            self.assertEqual(
                actual_opportunity_statement_types,
                expected_opportunity,
                f"Failed on {opportunity_index}th opportunity comparison",
            )

    @staticmethod
    def _get_method_ast() -> AST:
        return get_method_ast("ExampleFromPaper.java", "ExampleFromPaper", "grabManifests")

    _method_semantic = [
        objects_semantic("rcs.length", "manifests"),  # line 7
        objects_semantic("i", "rcs.length"),  # line 8
        objects_semantic("rec"),  # line 9
        objects_semantic("i", "rcs"),  # line 10
        StatementSemantic(used_objects={"rec", "rcs", "i"}, used_methods={"grabRes"}),  # line 11
        StatementSemantic(used_objects={"rec", "rcs", "i"}, used_methods={"grabNonFileSetRes"}),  # line 13
        objects_semantic("rec", "j", "length"),  # line 15
        StatementSemantic(used_objects={"name", "rec", "j"}, used_methods={"getName", "replace"}),  # line 16
        objects_semantic("rcs", "i"),  # line 17
        objects_semantic("afs", "rcs", "i"),  # line 18
        StatementSemantic(used_objects={"afs"}, used_methods={"equals", "getFullpath", "getProj"}),  # line 19
        StatementSemantic(used_objects={"name.afs"}, used_methods={"getFullpath", "getProj"}),  # line 20
        StatementSemantic(used_objects={"afs"}, used_methods={"equals", "getPref", "getProj"}),  # line 21
        StatementSemantic(used_objects={"afs", "pr"}, used_methods={"getPref", "getProj"}),  # line 22
        StatementSemantic(used_objects={"pr"}, used_methods={"endsWith"}),  # line 23
        objects_semantic("pr"),  # line 24
        objects_semantic("pr", "name"),  # line 26
        StatementSemantic(
            used_objects={"name", "MANIFEST_NAME"}, used_methods={"equalsIgnoreCase"}
        ),  # line 29
        objects_semantic("manifests", "i", "rec", "j"),  # line 30
        StatementSemantic(),  # line 31
        objects_semantic("manifests", "i"),  # line 34
        objects_semantic("manifests", "i"),  # line 35
        objects_semantic("manifests"),  # line 38
    ]

    _expected_extraction_opportunities = [
        [ASTNodeType.LOCAL_VARIABLE_DECLARATION, ASTNodeType.FOR_STATEMENT],  # lines 7-8
        [ASTNodeType.LOCAL_VARIABLE_DECLARATION],  # line 9
        [
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.FOR_STATEMENT,
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
        ],  # lines 10-16
        [
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.IF_STATEMENT,
        ],  # lines 17-29
        [ASTNodeType.STATEMENT_EXPRESSION],  # line 30
        [ASTNodeType.BREAK_STATEMENT],  # line 31
        [
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.RETURN_STATEMENT,
        ],  # lines 34-38
        [
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ASTNodeType.FOR_STATEMENT,
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.FOR_STATEMENT,
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
        ],  # lines 7-16
        [
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.BREAK_STATEMENT,
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.RETURN_STATEMENT,
        ],  # lines 30-38
        [
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ASTNodeType.FOR_STATEMENT,
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.FOR_STATEMENT,
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
            ASTNodeType.IF_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.STATEMENT_EXPRESSION,
            ASTNodeType.IF_STATEMENT,
        ],  # lines 7-29
    ]

    _expected_filtered_extraction_opportunities = [
        [ASTNodeType.LOCAL_VARIABLE_DECLARATION],  # line 9
        [ASTNodeType.STATEMENT_EXPRESSION],  # line 30
    ]
