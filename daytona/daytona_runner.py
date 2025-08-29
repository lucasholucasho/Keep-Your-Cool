from daytona import Daytona, DaytonaConfig

config = DaytonaConfig(api_key="dtn_4a440368d8e67bf85cee72c23873fc32f4f26cff50c572f43df864075fa66339")
daytona = Daytona(config)
sandbox = daytona.create()

response = sandbox.process.code_run('print("Hello World from code!")')

if response.exit_code != 0:
  print(f"Error: {response.exit_code} {response.result}")
else:
    print(response.result)

sandbox.delete()