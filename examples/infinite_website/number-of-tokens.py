from transformers import (
  AutoTokenizer
)

model_id = "nomic-ai/gpt4all-j"
model_kwargs = {}

tokenizer = AutoTokenizer.from_pretrained(model_id, **model_kwargs)

prompt = """<?xml version="1.0"?>
<ruleset id="HZRules"
	xmlns="http://windup.jboss.org/schema/jboss-ruleset"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://windup.jboss.org/schema/jboss-ruleset http://windup.jboss.org/schema/jboss-ruleset/windup-jboss-ruleset.xsd">

	<metadata>
		<description>
			This ruleset detects embedded hazelcast, which may be problematic
			when migrating an application to a cloud environment.
		</description>
		<dependencies>
			<addon id="org.jboss.windup.rules,windup-rules-javaee,3.0.0.Final" />
			<addon id="org.jboss.windup.rules,windup-rules-java,3.0.0.Final" />
		</dependencies>

		<targetTechnology id="cloud-readiness" />

		<tag>Hazelcast</tag>
	</metadata>
	<rules>
		<rule id="hazelcast-cloud-readiness-hz001">
			<when>
				<or>
					<javaclass
						references="com.hazelcast.config.JoinConfig.getMulticastConfig({*})">
						<location>METHOD_CALL</location>
					</javaclass>
					<javaclass
						references="com.hazelcast.config.JoinConfig.getTcpIpConfig({*})">
						<location>METHOD_CALL</location>
					</javaclass>
				</or>
			</when>
			<perform>
				<hint title="Embedded Hazelcast"
					category-id="cloud-mandatory" effort="3">
					<message> Consider using Kubernetes specific configuration.
					<![CDATA[
							// Example using Kubernetes specific configuration
							
							JoinConfig joinConfig = config.getNetworkConfig().getJoin();
							config.getKubernetesConfig().setEnabled(true)
							                      .setProperty("namespace", "namespace")
							                      .setProperty("service-name", "hazelcast-service");
							]]>
				</message>
				</hint>
			</perform>
		</rule>
		
		<rule id="hazelcast-cloud-readiness-hz002">
			<when>
				<project>
					<artifact groupId="com.hazelcast" artifactId="hazelcast"
						fromVersion="2.0.0" toVersion="4.2.7" />
				</project>
			</when>
			<perform>
			<hint title="Embedded Hazelcast dependencies"
					category-id="cloud-mandatory" effort="1">
					<message>The project uses hazelcast with the version between 2.0.0 and less than 5.0.0. Please use hazelcast 5.0 or above. </message>T
				</hint>
				
			</perform>
		</rule>
	</rules>
</ruleset>"""

inputs = tokenizer(prompt, return_tensors="pt")

print(inputs['input_ids'].size())