package org.openspaces.servicegrid.model.tasks;

import java.net.URI;

import org.openspaces.servicegrid.model.tasks.Task;

public class StartAgentTask extends Task {

	private String ipAddress;
	private URI agentExecutorId;

	public URI getAgentExecutorId() {
		return agentExecutorId;
	}

	public String getIpAddress() {
		return ipAddress;
	}

	public void setIpAddress(String ipAddress) {
		this.ipAddress = ipAddress;
	}

	public void setAgentExecutorId(URI agentExecutorId) {
		this.agentExecutorId = agentExecutorId;
	}

}
