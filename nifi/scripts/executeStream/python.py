from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from java.io import BufferedReader, InputStreamReader
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Read the CSV data from the content of the FlowFile
flowFile = session.get()
if flowFile is not None:
    flowFileInputStream = session.read(flowFile)
    csv_data = IOUtils.toString(flowFileInputStream, StandardCharsets.UTF_8)
    flowFileInputStream.close()

    # Create a DataFrame from the CSV data
    df = pd.read_csv(StringIO(csv_data))

    # Perform any processing on the DataFrame if needed

    # Convert the DataFrame to a PyArrow Table
    table = pa.Table.from_pandas(df)

    # Write the PyArrow Table to Parquet format
    parquet_data = pq.write_table(table).to_pybytes()

    # Set attributes for the new FlowFile
    new_flowFile = session.create()
    new_flowFile = session.putAttribute(
        new_flowFile,
        "filename",
        flowFile.getAttribute("filename").replace(".csv", ".parquet"),
    )

    # Write the Parquet data to the content of the new FlowFile
    new_flowFile = session.write(
        new_flowFile, lambda outputStream: outputStream.write(parquet_data)
    )

    # Transfer the new FlowFile to success relationship
    session.transfer(new_flowFile, REL_SUCCESS)

    # Transfer the original FlowFile to success relationship
    session.transfer(flowFile, REL_SUCCESS)
