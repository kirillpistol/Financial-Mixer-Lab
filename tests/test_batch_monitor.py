from app.batch_monitor import Station, simulate_batch

def test_bottleneck_limits_work():
    x=simulate_batch(1000,2,Station("A",100,.1),Station("B",80,.2))
    assert x["processed"]==160
    assert x["remaining"]==840
    assert x["expected_both_success"]==115.2

def test_empty_run():
    x=simulate_batch(0,1)
    assert x["processed"]==0

def test_invalid_rate():
    try:
        simulate_batch(10,1,Station("A",0,0),Station("B",5,0))
    except ValueError:
        return
    assert False
