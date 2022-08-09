<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:oebb="http://www.foo.org/">
	<xsl:strip-space elements="*"/>
    <xsl:template match="/stages/stage2/rollingstock/vehicles">
		<vehicles>
			<xsl:apply-templates select="*" />
		</vehicles>
	</xsl:template>
	
	<xsl:template match="/stages/stage2/rollingstock/vehicles/*">
		<xsl:element name="{local-name()}">
			<xsl:copy-of select="*| @*" />
			<xsl:variable name="elementID" select="@id"/>
			<xsl:copy-of select="/stages/stage1/rollingstock/vehicles/*[@id=$elementID]/oebb:bela" />
		</xsl:element>
	</xsl:template>
</xsl:stylesheet>