import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import com.google.gson.Gson;

public class OracleReader {

	private String host;
	private String port;
	private String service;
	private String username;
	private String password;
	private Connection db; // A connection to the database
	private Statement stmt; // Our statement to run queries with
	private DatabaseMetaData dbmd; // This is basically info the driver delivers
	private Gson gson;

	private class TableMetaData {
		public ArrayList<ColumnMetaData> columns;

		public TableMetaData() {
			columns = new ArrayList<ColumnMetaData>();
		}

		public void addValue(String columnName, String columnType,
				int columnSize) {
			columns.add(new ColumnMetaData(columnName, columnType, columnSize));
		}
	}

	private class ColumnMetaData {
		public String name;
		public String type;
		public int size;

		public ColumnMetaData(String columnName, String columnType,
				int columnSize) {
			name = columnName;
			type = columnType;
			size = columnSize;
		}

		public String toString() {
			return "name: " + name + ", type: " + type + ", size: " + size;
		}
	}

	private class TableData {
		public ArrayList<RowData> rows;

		public TableData() {
			rows = new ArrayList<RowData>();
		}

		public void addRow(RowData row) {
			rows.add(row);
		}
	}

	private class RowData {
		public Map<String, String> fieldValues;

		public RowData() {
			fieldValues = new HashMap<String, String>();
		}

		public void addValue(String columnName, String columnValue) {
			fieldValues.put(columnName, columnValue);
		}

		public String toString() {
			return fieldValues.toString();
		}
	}

	private class TableCount {
		public int rowCount;

		public TableCount(int count) {
			rowCount = count;
		}

		public String toString() {
			return "rowCount: " + rowCount;
		}
	}

	public OracleReader() {
		// initialize Gson object
		gson = new Gson();
	}

	public boolean connect(String h, String p, String srv, String usr,
			String pwd) {
		host = h;
		port = p;
		service = srv;
		username = usr;
		password = pwd;
		// host = "10.1.22.71";
		// port = "1522";
		// service = "VIS";
		// username = "apps";
		// password = "apps";
		try {
			Class.forName("oracle.jdbc.driver.OracleDriver");
			String dbConnectString = "jdbc:oracle:thin:@//" + host + ":" + port
					+ "/" + service;
			System.out.println(dbConnectString);
			db = DriverManager.getConnection(dbConnectString, username,
					password);
			dbmd = db.getMetaData(); // get MetaData to confirm connection
			System.out
					.println("Connection to " + dbmd.getDatabaseProductName()
							+ " " + dbmd.getDatabaseProductVersion()
							+ " successful.\n");
			return true;
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// e.printStackTrace();
			return false;
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			// e.printStackTrace();
			return false;
		}
	}

	public String getStructureJSON(String query) throws SQLException {
		try {
			stmt = db.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			ResultSetMetaData rsmd = rs.getMetaData();
			int numColumns = rsmd.getColumnCount();
			TableMetaData md = new TableMetaData();
			for (int i = 0; i < numColumns; i++) {
				md.addValue(rsmd.getColumnName(i + 1).toLowerCase(), rsmd
						.getColumnTypeName(i + 1).toLowerCase(), rsmd
						.getColumnDisplaySize(i + 1));
			}
			String tableMetaDataString = gson.toJson(md);
			return tableMetaDataString;
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// e.printStackTrace();
			throw new SQLException();
		}
	}

	public int getCount(String query) throws SQLException {
		try {
			stmt = db.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			int size = 0;
			while (rs.next()) {
				size++;
			}
			return size;
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// e.printStackTrace();
			// return 0;
			throw new SQLException();
		}
	}

	public String getCountJSON(String query) throws SQLException {
		try {
			stmt = db.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			int size = 0;
			while (rs.next()) {
				size++;
			}
			TableCount tc = new TableCount(size);
			String tableCountString = gson.toJson(tc);
			return tableCountString;
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// e.printStackTrace();
			// return null;
			throw new SQLException();
		}
	}

	public String getDataJSON(String query, int startRow, int numRows)
			throws SQLException {
		try {
			stmt = db.createStatement();
			String limitQuery = String
					.format(
							"select * from 	( select a.*, ROWNUM rnum from ( %s ) a where ROWNUM <= %d ) where rnum  >= %d",
							query, (startRow + numRows - 1), startRow);

			// System.out.println(limitQuery);
			// ResultSet rs = stmt.executeQuery(query);
			ResultSet rs = stmt.executeQuery(limitQuery);
			ResultSetMetaData rsmd = rs.getMetaData();
			int numColumns = rsmd.getColumnCount();
			TableData td = new TableData();
			String columnName, columnValue;
			while (rs.next()) {
				RowData rd = new RowData();
				for (int i = 0; i < numColumns; i++) {
					columnName = rsmd.getColumnName(i + 1).toLowerCase();
					columnValue = rs.getString(i + 1);
					rd.addValue(columnName, columnValue);
				}
				td.addRow(rd);
			}
			String tableDataString = gson.toJson(td);
			return tableDataString;
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// e.printStackTrace();
			// return null;
			throw new SQLException();
		}
	}
}
