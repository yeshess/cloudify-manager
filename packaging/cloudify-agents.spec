Name:           cloudify-agents
Version:        %{CLOUDIFY_VERSION}
Release:        %{CLOUDIFY_PACKAGE_RELEASE}%{?dist}
Summary:        Cloudify's agents bundle
Group:          Applications/Multimedia
License:        Apache 2.0
URL:            https://github.com/cloudify-cosmo/cloudify-agent
Vendor:         Gigaspaces Inc.
Packager:       Gigaspaces Inc.

BuildRequires:  python >= 2.7
Requires(pre):  shadow-utils


%description
Cloudify Agent packages

%prep

curl https://raw.githubusercontent.com/cloudify-cosmo/cloudify-versions/master/packages-urls/agent-packages.yaml > /tmp/agents-list.txt

%build

mkdir -p /opt/manager/resources/packages/agents
cd /opt/manager/resources/packages/agents
xargs -I url curl -O url </tmp/agents-list.txt
rm /tmp/agents-list.txt

python -c 'import os

def splitext(filename):
    # not using os.path.splitext as it would return .gz instead of .tar.gz
    if filename.endswith(".tar.gz"):
        return ".tar.gz"
    elif filename.endswith(".exe"):
        return ".exe"
    else:
        raise ValueError("Unknown agent format for {0}. "
            "Must be either tar.gz or exe".format(filename))

def normalize_agent_name(filename):
    return filename.split("_", 1)[0].lower()

for fn in os.listdir("."):
    extension = splitext(fn)
    os.rename(fn, normalize_agent_name(fn) + extension)
'

%install
mv /opt %{buildroot}/opt

%pre
groupadd -fr cfyuser
getent passwd cfyuser >/dev/null || useradd -r -g cfyuser -d /etc/cloudify -s /sbin/nologin cfyuser


%post
%preun
%postun


%files
%attr(750,cfyuser,adm) /opt/manager/resources/packages/agents
