import javax.swing.*;
import java.awt.*;

public class LoginPrompt extends JPanel {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	final int NUMFIELDS = 2;
	private JTextField[] fields;

	// Create a form with the specified labels, tooltips, and sizes.
	public LoginPrompt() {
		super(new BorderLayout());

		JPanel labelPanel = new JPanel(new GridLayout(NUMFIELDS, 1));
		JPanel fieldPanel = new JPanel(new GridLayout(NUMFIELDS, 1));
		add(labelPanel, BorderLayout.WEST);
		add(fieldPanel, BorderLayout.CENTER);
		fields = new JTextField[NUMFIELDS];

		// add email field
		JTextField emailField = new JTextField();
		emailField.setColumns(20);
		JLabel emailLab = new JLabel("Email", JLabel.RIGHT);
		emailLab.setLabelFor(emailField);
		labelPanel.add(emailLab);
		JPanel emailP = new JPanel(new FlowLayout(FlowLayout.LEFT));
		emailP.add(emailField);
		fieldPanel.add(emailP);
		fields[0] = emailField;

		// add password field
		JPasswordField passwordField = new JPasswordField();
		passwordField.setColumns(20);
		JLabel passwordLab = new JLabel("Password", JLabel.RIGHT);
		passwordLab.setLabelFor(passwordField);
		labelPanel.add(passwordLab);
		JPanel passwordP = new JPanel(new FlowLayout(FlowLayout.LEFT));
		passwordP.add(passwordField);
		fieldPanel.add(passwordP);
		fields[1] = passwordField;
	}

	public String getText(int i) {
		return (fields[i].getText());
	}

}