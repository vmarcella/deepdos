# deepdos.tests.test_processes

## proc_close_success
```python
proc_close_success()
```

Successfully closed command

## proc_close_fail
```python
proc_close_fail()
```

Failed to close command

## stub_pcap_line_data
```python
stub_pcap_line_data()
```

Stub the pcap line data inside of the test

## ProcessTests
```python
ProcessTests(self, methodName='runTest')
```

### test_successful_capture_pcap
```python
ProcessTests.test_successful_capture_pcap(self, mock_process)
```

Test to ensure that pcap succeeds under normal capture

### test_failed_pcap
```python
ProcessTests.test_failed_pcap(self, mock_process)
```

Test to ensure that pcap fails when process closes

### test_successfull_find_deepdos
```python
ProcessTests.test_successfull_find_deepdos(self, mock_proc)
```

Test a successful run for finding deepdos

# deepdos.tests.test_network

Network usage model

# deepdos.tests.test_conf

# __init__
```python
__init__(*args, **kwargs)
```
Initialize self.  See help(type(self)) for accurate signature.
