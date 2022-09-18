from ficsit.effeciency_calculations import *
from ficsit.effeciency import CompareRecipes
from ficsit.components import *


class Test_calculate_produced_per_minute:
    def setup(self):
        pass

    def teardown(self):
        pass

    def test_returns_a_float(self):
        # Arrange, Act
        result = items_per_minute(item_count=10, time=45)

        # Assert
        assert isinstance(result, float)

    def test_returns_valid_answer_with_sub_60_second_production_time(self):
        # Arrange, Act
        result = items_per_minute(item_count=2, time=30)

        # Assert
        assert result == 4.0

    def test_returns_valid_answer_with_greater_than_60_second_production_time(self):
        # Arrange, Act
        result = items_per_minute(item_count=1, time=120)

        # Assert
        assert result == 0.5


class Test_calculate_components_per_minute:
    def setup(self):
        self.test_components = {"testOne": 3, "testTwo": 1}

    def teardown(self):
        del self.test_components

    def test_returns_dictionary(self):
        # Arrange, Act
        result = calculate_components_per_minute(
            components=self.test_components, time=30
        )

        # Assert
        assert isinstance(result, dict)

    def test_does_not_modify_original_dict(self):
        # Arrange, Act
        result = calculate_components_per_minute(
            components=self.test_components, time=30
        )

        # Assert
        assert result != self.test_components

    def test_calculates_item_per_minute_for_each_component(self):
        # Arrange, Act
        result = calculate_components_per_minute(
            components=self.test_components, time=30
        )

        # Assert
        assert result["testOne"] == 6.0
        assert result["testTwo"] == 2.0


class Test_Effeciency:
    def setup(self):
        self.test_class = CompareRecipes(ManufacturedComponents.IRON_PLATE)

    def teardown(self):
        del self.test_class

    def test_is_all_components_returns_true_if_all_base_components(self):
        # Arrange:
        test_ingredients = {BaseComponents.IRON: 4, BaseComponents.LIMESTONE: 4}

        # Act, assert
        assert self.test_class._is_all_components(test_ingredients)

    def test_is_all_components_returns_false_if_any_not_base_component(self):
        # Arrange:
        test_ingredients = {
            ManufacturedComponents.IRON_PLATE: 4,
            BaseComponents.LIMESTONE: 4,
        }

        # Act, assert
        assert not self.test_class._is_all_components(test_ingredients)
