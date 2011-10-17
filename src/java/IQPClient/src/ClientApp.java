import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.Date;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

public class ClientApp {

	public final int ROWLIMIT = 1000;
	public Uploader uploader;
	public OracleReader oracleReader;
	String logFileName = "iqpclientlog.txt";
	BufferedWriter out;
	Date date;

	public ClientApp() {
		uploader = new Uploader();
		oracleReader = new OracleReader();
		date = new java.util.Date();

		try {
			out = new BufferedWriter(new FileWriter(logFileName, true));
			out.newLine();
			System.out.println();
			out.append("------------------------------------------");
			System.out.print("------------------------------------------");
			out.newLine();
			System.out.println();
			date = new java.util.Date();
			out.append(new Timestamp(date.getTime()) + " - "
					+ "starting new upload.");
			System.out.print(new Timestamp(date.getTime()) + " - "
					+ "starting new upload.");
			out.newLine();
			System.out.println();
			// out.append("starting new upload.");
			// out.newLine();
			out.flush();
			// out.close();
		} catch (IOException e) {
		}

	}

	public final static void main(String[] args) throws Exception {
		ClientApp c = new ClientApp();
		c.login();
	}

	public void login() {
		final LoginPrompt form = new LoginPrompt();
		JButton submit = new JButton("Login");
		final JFrame f = new JFrame("IQP Server Login");
		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		f.getContentPane().add(form, BorderLayout.NORTH);
		JPanel p = new JPanel();
		p.add(submit);
		f.getContentPane().add(p, BorderLayout.SOUTH);
		f.pack();
		submit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent evt) {
				f.setVisible(false);
				String email = form.getText(0);
				String password = form.getText(1);
				boolean loginSuccess = uploader.login(email, password);
				try {
					if (loginSuccess) {
						date = new java.util.Date();
						out.append(new Timestamp(date.getTime()) + " - "
								+ "connect to IQP server success");
						System.out.print(new Timestamp(date.getTime()) + " - "
								+ "connect to IQP server success");
						out.newLine();
						System.out.println();
						connectToOracle();
					} else {
						date = new java.util.Date();
						out.append(new Timestamp(date.getTime()) + " - "
								+ "connect to IQP server failure");
						System.out.print(new Timestamp(date.getTime()) + " - "
								+ "connect to IQP server failure");
						out.newLine();
						System.out.println();
						JOptionPane.showMessageDialog(f,
								"Unable to login to IQP Server.",
								"Login Error", JOptionPane.ERROR_MESSAGE);
					}
				} catch (IOException e) {
				}
				f.dispose();
			}
		});
		f.setVisible(true);
	}

	public void connectToOracle() {
		final OracleConnectPrompt form = new OracleConnectPrompt();
		JButton submit = new JButton("Connect");
		final JFrame f = new JFrame("Oracle DB Connection");
		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		f.getContentPane().add(form, BorderLayout.NORTH);
		JPanel p = new JPanel();
		p.add(submit);
		f.getContentPane().add(p, BorderLayout.SOUTH);
		f.pack();
		submit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent evt) {
				f.setVisible(false);
				String host = form.getText(0);
				String port = form.getText(1);
				String service = form.getText(2);
				String username = form.getText(3);
				String password = form.getText(4);
				boolean oracleConnectSuccess;
				try {
					oracleConnectSuccess = oracleReader.connect(host, port,
							service, username, password);
					if (oracleConnectSuccess) {
						date = new java.util.Date();
						out.append(new Timestamp(date.getTime()) + " - "
								+ "connect to Oracle DB success");
						System.out.print(new Timestamp(date.getTime()) + " - "
								+ "connect to Oracle DB success");
						out.newLine();
						System.out.println();
						startUpload();
					} else {
						date = new java.util.Date();
						out.append(new Timestamp(date.getTime()) + " - "
								+ "connect to Oracle DB failure");
						System.out.print(new Timestamp(date.getTime()) + " - "
								+ "connect to Oracle DB failure");
						out.newLine();
						System.out.println();
						JOptionPane.showMessageDialog(f,
								"Unable to connect to Oracle DB.", "DB Error",
								JOptionPane.ERROR_MESSAGE);
					}
				} catch (IOException e) {
				}
				f.dispose();
			}
		});
		f.setVisible(true);
	}

	public void startUpload() {
		int[] allScenarioIDs = uploader.getAllScenarios();
		int scenarioID;
		String scenarioQuery, modScenarioQuery, queryResultStructure, queryResultData;
		try {
			for (int i = 0; i < allScenarioIDs.length; i++) {
				scenarioID = allScenarioIDs[i];
				date = new java.util.Date();
				out.append(new Timestamp(date.getTime()) + " - " + "scn id: "
						+ scenarioID + " starting...");
				System.out.print(new Timestamp(date.getTime()) + " - "
						+ "scn id: " + scenarioID + " starting...");
				out.newLine();
				System.out.println();
				out.flush();
				scenarioQuery = uploader.getScenarioQuery(scenarioID);
				if (!scenarioQuery.isEmpty()) {
					modScenarioQuery = scenarioQuery.replace("@XXX", "");
					modScenarioQuery = modScenarioQuery.replace("@xxx", "");
					try {
						queryResultStructure = oracleReader
								.getStructureJSON(modScenarioQuery);
						// System.out.println(queryResultStructure);
						uploader.sendQueryResultStructure(scenarioID,
								queryResultStructure);
						int resultSize = oracleReader
								.getCount(modScenarioQuery);
						String queryResultCount = oracleReader
								.getCountJSON(modScenarioQuery);
						uploader.sendQueryResultCount(scenarioID,
								queryResultCount);
						for (int currentRow = 1; currentRow <= resultSize; currentRow = currentRow
								+ ROWLIMIT) {
							queryResultData = oracleReader.getDataJSON(
									modScenarioQuery, currentRow, ROWLIMIT);
							if (queryResultData != null) {
								uploader.sendQueryResultData(scenarioID,
										queryResultData);
							}
						}
						date = new java.util.Date();
						out.append(new Timestamp(date.getTime()) + " - "
								+ "scn id: " + scenarioID + " has uploaded "
								+ resultSize + " rows.");
						System.out.print(new Timestamp(date.getTime()) + " - "
								+ "scn id: " + scenarioID + " has uploaded "
								+ resultSize + " rows.");
						out.newLine();
						System.out.println();
						out.flush();
					} catch (SQLException e) {
						date = new java.util.Date();
						out
								.append(new Timestamp(date.getTime())
										+ " - "
										+ "scn id: "
										+ scenarioID
										+ " has an invalid query, caused an exception.");
						System.out
								.print(new Timestamp(date.getTime())
										+ " - "
										+ "scn id: "
										+ scenarioID
										+ " has an invalid query, caused an exception.");
						out.newLine();
						System.out.println();
						out.flush();
					}
				} else {
					date = new java.util.Date();
					out.append(new Timestamp(date.getTime()) + " - "
							+ "scn id: " + scenarioID + " has no query.");
					System.out.print(new Timestamp(date.getTime()) + " - "
							+ "scn id: " + scenarioID + " has no query.");
					out.newLine();
					System.out.println();
					out.flush();
				}
			}
			date = new java.util.Date();
			out.append(new Timestamp(date.getTime()) + " - "
					+ "finished all scenarios.");
			System.out.print(new Timestamp(date.getTime()) + " - "
					+ "finished all scenarios.");
			out.newLine();
			System.out.println();
			out.newLine();
			System.out.println();
			out.flush();
		} catch (IOException e) {
		}
	}
}
