from rest_framework import serializers
from web3 import Web3

from symbol.models import Symbol, BalanceModifier, Balance, Chain
from symbol.scanner import Scanner


class BalanceModifierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceModifier
        fields = '__all__'
        read_only_fields = ('symbol',)

    def validate(self, attrs):
        params_types = Scanner.get_params_types(attrs['function_signature'])

        if len(params_types) != len(attrs['params_mask']):
            raise serializers.ValidationError("Invalid params mask length")

        attrs['contract_address'] = Web3.to_checksum_address(attrs['contract_address'])
        return attrs


class SymbolCreateSerializer(serializers.ModelSerializer):
    modifiers = BalanceModifierCreateSerializer(many=True)

    class Meta:
        model = Symbol
        fields = '__all__'
        read_only_fields = ('owner',)

    def create(self, validated_data):
        modifiers = validated_data.pop('modifiers')

        symbol = Symbol.objects.create(**validated_data)

        for modifier in modifiers:
            modifier['contract_address'] = Web3.to_checksum_address(modifier['contract_address'])
            BalanceModifier.objects.create(
                **modifier,
                symbol=symbol
            )

        return symbol


class BalanceListSerializer(serializers.ModelSerializer):
    symbol_name = serializers.CharField(source='symbol.name')
    class Meta:
        model = Balance
        fields = ('symbol_name', 'value')


class SymbolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ('id', 'name')

class ChainListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chain
        fields = ('id', 'name', 'chain_id')
