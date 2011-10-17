import javax.swing.*;
import java.awt.*;

public class OracleConnectPrompt extends JPanel {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	final int NUMFIELDS = 5;
	private JTextField[] fields;

	// Create a form with the specified labels, tooltips, and sizes.
	public OracleConnectPrompt() {
		super(new BorderLayout());

		JPanel labelPanel = new JPanel(new GridLayout(NUMFIELDS, 1));
		JPanel fieldPanel = new JPanel(new GridLayout(NUMFIELDS, 1));
		add(labelPanel, BorderLayout.WEST);
		add(fieldPanel, BorderLayout.CENTER);
		fields = new JTextField[NUMFIELDS];

		// add host field
		JTextField hostField = new JTextField();
		hostField.setColumns(20);
		JLabel hostLab = new JLabel("Host", JLabel.RIGHT);
		hostLab.setLabelFor(hostField);
		labelPanel.add(hostLab);
		JPanel hostP = new JPanel(new FlowLayout(FlowLayout.LEFT));
		hostP.add(hostField);
		fieldPanel.add(hostP);
		fields[0] = hostField;

		// add port field
		JTextField portField = new JTextField();
		portField.setColumns(20);
		JLabel portLab = new JLabel("Port", JLabel.RIGHT);
		portLab.setLabelFor(portField);
		labelPanel.add(portLab);
		JPanel portP = new JPanel(new FlowLayout(FlowLayout.LEFT));
		portP.add(portField);
		fieldPanel.add(portP);
		fields[1] = portField;

		// add service field
		JTextField serviceField = new JTextField();
		serviceField.setColumns(20);
		JLabel serviceLab = new JLabel("Service", JLabel.RIGHT);
		serviceLab.setLabelFor(serviceField);
		labelPanel.add(serviceLab);
		JPanel serviceP = new JPanel(new FlowLayout(FlowLayout.LEFT));
		serviceP.add(serviceField);
		fieldPanel.add(serviceP);
		fields[2] = serviceField;

		// add username field
		JTextField usernameField = new JTextField();
		usernameField.setColumns(20);
		JLabel usernameLab = new JLabel("Username", JLabel.RIGHT);
		usernameLab.setLabelFor(usernameField);
		labelPanel.add(usernameLab);
		JPanel usernameP = new JPanel(new FlowLayout(FlowLayout.LEFT));
		usernameP.add(usernameField);
		fieldPanel.add(usernameP);
		fields[3] = usernameField;

		// add password field
		JPasswordField passwordField = new JPasswordField();
		passwordField.setColumns(20);
		JLabel passwordLab = new JLabel("Password", JLabel.RIGHT);
		passwordLab.setLabelFor(passwordField);
		labelPanel.add(passwordLab);
		JPanel passwordP = new JPanel(new FlowLayout(FlowLayout.LEFT));
		passwordP.add(passwordField);
		fieldPanel.add(passwordP);
		fields[4] = passwordField;
	}

	public String getText(int i) {
		return (fields[i].getText());
	}

}