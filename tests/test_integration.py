from src.models import Apartment
from src.manager import Manager
from src.models import Parameters
from src.models import Bill


def test_load_data():
    parameters = Parameters()
    manager = Manager(parameters)
    assert isinstance(manager.apartments, dict)
    assert isinstance(manager.tenants, dict)
    assert isinstance(manager.transfers, list)
    assert isinstance(manager.bills, list)

    for apartment_key, apartment in manager.apartments.items():
        assert isinstance(apartment, Apartment)
        assert apartment.key == apartment_key

def test_tenants_in_manager():
    parameters = Parameters()
    manager = Manager(parameters)
    assert len(manager.tenants) > 0
    names = [tenant.name for tenant in manager.tenants.values()]
    for tenant in ['Jan Nowak', 'Adam Kowalski', 'Ewa Adamska']:
        assert tenant in names

def test_if_tenants_have_valid_apartment_keys():
    parameters = Parameters()
    manager = Manager(parameters)
    assert manager.check_tenants_apartment_keys() == True

    manager.tenants['tenant-1'].apartment = 'invalid-key'
    assert manager.check_tenants_apartment_keys() == False

def test_get_apartment_costs():
    parameters = Parameters()
    manager = Manager(parameters)

    manager.bills = [Bill(apartment='A1',amount_pln=150,date_due='2024-03-05',settlement_year=2024,settlement_month=3, type='woda'),
                     Bill(apartment='A1',amount_pln=132,date_due='2024-03-11',settlement_year=2024,settlement_month=3, type='prad'),
                     Bill(apartment='A2',amount_pln=1,date_due='2024-03-12',settlement_year=2024,settlement_month=3, type='woda'),
                     Bill(apartment='A2',amount_pln=1000,date_due='2024-03-13',settlement_year=2024,settlement_month=3, type='gaz')]
    
    manager.apartments = {'A1': Apartment(key='A1', name='Apartment 1',location='Chartowo', area_m2=50,rooms={}),
                          'A2': Apartment(key='A2', name='Apartment 2',location='Siemianowiceslaskie', area_m2=50,rooms={})}

    assert manager.get_apartment_costs('A532',2024,3) == 0
    assert manager.get_apartment_costs('A1',2024,3) == 282
    assert manager.get_apartment_costs('A1',2024,4) == 0